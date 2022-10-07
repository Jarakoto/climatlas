import LocationType from './LocationType'
import validate from './location.validator'
import { AxiosResponse } from 'axios'

export default class Location {
  type: LocationType = LocationType.UNKNOWN
  name: string
  label: string
  coordinates: [number, number]

  constructor (type: LocationType, name: string, label: string, coordinates: [number, number]) {
    this.type = type
    this.name = name
    this.label = label
    this.coordinates = coordinates
  }

  renderType () {
    switch (this.type) {
      case LocationType.UNKNOWN:
        return 'inconnu'
      case LocationType.STREET:
        return 'rue'
      case LocationType.LOCALITY:
        return 'localité'
      case LocationType.MUNICIPALITY:
        return 'municipalité'
      case LocationType.ADDRESS:
        return 'adresse'
    }
  }

  static createFromApi (fetchedData: AxiosResponse<unknown>): Location[] {
    if (validate(fetchedData.data)) {
      return fetchedData.data.features.map((feature) => {
        const locationType = feature.properties.type ? feature.properties.type : LocationType.ADDRESS
        const name = feature.properties.name
        const label = feature.properties.label
        const coordinates = feature.geometry.coordinates as [number, number]
        return new Location(locationType, name, label, coordinates)
      })
    } else {
      throw validate.errors
    }
  }
}
