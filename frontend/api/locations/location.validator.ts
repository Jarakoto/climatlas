import Ajv, { JSONSchemaType } from 'ajv'
import LocationType from './LocationType'

const ajv = new Ajv()

interface Properties {
  name: string
  label: string
  type?: LocationType
}

interface Geometry {
  coordinates: number[]
}

export interface Feature {
  geometry: Geometry
  properties: Properties
}

export interface FeatureCollection {
  features: Feature[]
}

const schema: JSONSchemaType<FeatureCollection> = {
  type: 'object',
  properties: {
    features: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          geometry: {
            type: 'object',
            properties: {
              coordinates: {
                type: 'array',
                items: {
                  type: 'number'
                },
                minItems: 2,
                maxItems: 2
              }
            },
            required: ['coordinates']
          },
          properties: {
            type: 'object',
            properties: {
              name: { type: 'string' },
              type: {
                type: 'string',
                enum: Object.values(LocationType),
                nullable: true
              },
              label: { type: 'string' }
            },
            required: ['name', 'label']
          }
        },
        required: ['properties', 'geometry']
      }
    }
  },
  required: ['features']
}

export default ajv.compile(schema)
