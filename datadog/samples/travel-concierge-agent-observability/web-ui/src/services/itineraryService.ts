import { generateClient } from 'aws-amplify/data'
import type { Schema } from '../../../amplify/data/resource'

const client = generateClient<Schema>()

export interface ItineraryItem {
  id: string
  user_id: string
  type: 'flight' | 'hotel' | 'activity' | 'restaurant' | 'transport'
  title: string
  location?: string
  price?: string
  date?: string
  time_of_day?: 'morning' | 'afternoon' | 'evening'
  details?: string
  description?: string
  createdAt?: string
  updatedAt?: string
}

export const getItineraryItems = async (userId: string): Promise<ItineraryItem[]> => {
  try {
    console.log('🗂️ Fetching itinerary items for userId:', userId);
    
    const itineraryResponse = await client.models.Itinerary.list({
      filter: {
        user_id: { eq: userId }
      }
    })

    console.log('🗂️ Itinerary response:', {
      data: itineraryResponse.data,
      errors: itineraryResponse.errors,
      count: itineraryResponse.data?.length || 0
    });

    const items = (itineraryResponse.data || []) as ItineraryItem[]
    console.log(`🗂️ Found ${items.length} itinerary items`);
    return items
  } catch (error) {
    console.error('Error fetching itinerary:', error)
    return []
  }
}

export const deleteItineraryItem = async (itemId: string): Promise<boolean> => {
  console.log('🗑️ Attempting to delete item:', itemId)
  try {
    const result = await client.models.Itinerary.delete({ id: itemId })
    console.log('🗑️ Delete result:', result)
    return true
  } catch (error) {
    console.error('❌ Error deleting itinerary item:', error)
    return false
  }
}
