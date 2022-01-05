/* eslint-disable no-unused-vars */
enum LocationType {
  MUNICIPALITY = 'municipality',
  LOCALITY = 'locality',
  ADDRESS = 'address',
  STREET = 'street',
  UNKNOWN = 'unknown'
}

export const getLocationPriority = (locationType: LocationType) => {
  switch (locationType) {
    case LocationType.UNKNOWN:
      return -1
    case LocationType.STREET:
      return 0
    case LocationType.LOCALITY:
      return 1
    case LocationType.MUNICIPALITY:
      return 2
    case LocationType.ADDRESS:
      return 3
  }
}

export default LocationType
