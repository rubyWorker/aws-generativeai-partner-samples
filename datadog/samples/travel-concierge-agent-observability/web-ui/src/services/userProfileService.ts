import { generateClient } from 'aws-amplify/data'
import type { Schema } from '../../../amplify/data/resource'

const client = generateClient<Schema>()

export interface UserPreferences {
  travel: {
    budget_range: string
    interests: string[]
    accommodation_type: string
    travel_style: string
  }
  communication: {
    notifications: boolean
    email_updates: boolean
    language: string
  }
}

export interface UserProfileData {
  id?: string
  userId: string
  name?: string
  email?: string
  address?: string
  notes?: string
  onboardingCompleted: boolean
  preferences?: UserPreferences
  createdAt?: string
  updatedAt?: string
}

/**
 * User Profile Service using AppSync GraphQL
 */
export const userProfileService = {
  /**
   * Create a new user profile
   */
  async createUserProfile(
    email: string,
    name: string,
    preferences: UserPreferences,
    userId?: string,
    _address?: string
  ): Promise<UserProfileData> {
    const response = await client.models.UserProfile.create({
      userId: userId || 'current-user',
      name,
      email,
      onboardingCompleted: true,
      preferences: JSON.stringify(preferences)
    })

    if (response.errors && response.errors.length > 0) {
      throw new Error(`Failed to create user profile: ${response.errors[0].message}`)
    }

    const profile = response.data as any

    return {
      id: profile?.id,
      userId: profile?.userId || userId || 'current-user',
      name: profile?.name || name,
      email: profile?.email || email,
      onboardingCompleted: profile?.onboardingCompleted || true,
      preferences: profile?.preferences ? JSON.parse(profile.preferences) : preferences,
      createdAt: profile?.createdAt,
      updatedAt: profile?.updatedAt
    }
  },

  /**
   * Get user profile by user ID
   */
  async getUserProfile(userId: string): Promise<UserProfileData | null> {
    const response = await client.models.UserProfile.list({
      filter: {
        userId: { eq: userId }
      }
    })

    if (response.errors && response.errors.length > 0) {
      throw new Error(`Failed to get user profile: ${response.errors[0].message}`)
    }

    const profiles = response.data || []
    if (profiles.length === 0) {
      return null
    }

    const profile = profiles[0]
    
    // Debug: log raw preferences from DynamoDB
    console.log('🔍 Raw profile.preferences type:', typeof profile.preferences)
    console.log('🔍 Raw profile.preferences:', profile.preferences)

    // Handle preferences - could be string (needs parsing) or already an object
    let parsedPreferences = undefined
    if (profile.preferences) {
      if (typeof profile.preferences === 'string') {
        parsedPreferences = JSON.parse(profile.preferences)
      } else {
        parsedPreferences = profile.preferences
      }
    }
    console.log('🔍 Parsed preferences:', parsedPreferences)

    return {
      id: profile.id,
      userId: profile.userId,
      name: profile.name || undefined,
      email: profile.email || undefined,
      address: profile.address || undefined,
      notes: profile.notes || undefined,
      onboardingCompleted: profile.onboardingCompleted || false,
      preferences: parsedPreferences,
      createdAt: profile.createdAt || undefined,
      updatedAt: profile.updatedAt || undefined
    }
  },

  /**
   * Update user profile
   */
  async updateUserProfile(
    userId: string,
    updates: Partial<Omit<UserProfileData, 'id' | 'userId' | 'createdAt' | 'updatedAt'>>
  ): Promise<UserProfileData> {
    const existingProfile = await this.getUserProfile(userId)
    if (!existingProfile || !existingProfile.id) {
      throw new Error('Profile not found for update')
    }

    const updateData: any = {}
    if (updates.name !== undefined) updateData.name = updates.name
    if (updates.email !== undefined) updateData.email = updates.email
    if (updates.address !== undefined) updateData.address = updates.address
    if ((updates as any).notes !== undefined) updateData.notes = (updates as any).notes
    if (updates.onboardingCompleted !== undefined) updateData.onboardingCompleted = updates.onboardingCompleted
    if (updates.preferences !== undefined) updateData.preferences = JSON.stringify(updates.preferences)

    const response = await client.models.UserProfile.update({
      id: existingProfile.id,
      ...updateData
    })

    if (response.errors && response.errors.length > 0) {
      throw new Error(`Failed to update user profile: ${response.errors[0].message}`)
    }

    const profile = response.data as any

    return {
      id: profile?.id,
      userId: profile?.userId || userId,
      name: profile?.name || undefined,
      email: profile?.email || undefined,
      address: profile?.address || undefined,
      notes: profile?.notes || undefined,
      onboardingCompleted: profile?.onboardingCompleted || false,
      preferences: profile?.preferences ? JSON.parse(profile.preferences) : undefined,
      createdAt: profile?.createdAt,
      updatedAt: profile?.updatedAt
    }
  },

  /**
   * Delete user profile
   */
  async deleteUserProfile(userId: string): Promise<void> {
    const existingProfile = await this.getUserProfile(userId)
    if (!existingProfile || !existingProfile.id) {
      return
    }

    const response = await client.models.UserProfile.delete({
      id: existingProfile.id
    })

    if (response.errors && response.errors.length > 0) {
      throw new Error(`Failed to delete user profile: ${response.errors[0].message}`)
    }
  }
}
