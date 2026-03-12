import { useState, useEffect } from 'react'
import { userProfileService, UserPreferences, UserProfileData } from '../services/userProfileService'

interface User {
  username: string
  email?: string
  userId: string
  name?: string
}

interface UserProfileProps {
  user: User
  isOpen: boolean
  onClose: () => void
}

const UserProfile = ({ user, isOpen, onClose }: UserProfileProps) => {
  const [profile, setProfile] = useState<UserProfileData | null>(null)
  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [editMode, setEditMode] = useState(false)
  const [formData, setFormData] = useState({
    name: user.name || user.username,
    email: user.email || '',
    address: '',
    notes: '',
    travelBudget: 'mid-range',
    travelInterests: [] as string[],
    accommodationType: 'hotels',
    travelStyle: 'balanced',
    notifications: true,
    emailUpdates: true,
  })

  const travelInterestOptions = [
    'Adventure', 'Culture', 'Food & Dining', 'Nature', 'History', 
    'Art & Museums', 'Nightlife', 'Beach', 'Mountains'
  ]

  // Load user profile when modal opens
  useEffect(() => {
    if (isOpen) {
      loadProfile()
    }
  }, [isOpen, user.userId])

  const loadProfile = async () => {
    try {
      setLoading(true)
      setError(null)
      const userProfile = await userProfileService.getUserProfile(user.userId)
      setProfile(userProfile)
      
      if (userProfile && userProfile.preferences) {
        setFormData({
          name: userProfile.name || user.username,
          email: userProfile.email || user.email || '',
          address: userProfile.address || '',
          notes: (userProfile as any).notes || '',
          travelBudget: userProfile.preferences.travel?.budget_range || 'mid-range',
          travelInterests: userProfile.preferences.travel?.interests || [],
          accommodationType: userProfile.preferences.travel?.accommodation_type || 'hotels',
          travelStyle: userProfile.preferences.travel?.travel_style || 'balanced',
          notifications: userProfile.preferences.communication?.notifications || true,
          emailUpdates: userProfile.preferences.communication?.email_updates || true,
        })
      }
    } catch (err) {
      console.error('Error loading profile:', err)
      setError('Failed to load profile')
    } finally {
      setLoading(false)
    }
  }

  const handleInterestToggle = (interest: string) => {
    setFormData(prev => ({
      ...prev,
      travelInterests: prev.travelInterests.includes(interest)
        ? prev.travelInterests.filter(i => i !== interest)
        : [...prev.travelInterests, interest]
    }))
  }

  const handleSave = async () => {
    setSaving(true)
    try {
      const preferences: UserPreferences = {
        travel: {
          budget_range: formData.travelBudget,
          interests: formData.travelInterests,
          accommodation_type: formData.accommodationType,
          travel_style: formData.travelStyle
        },
        communication: {
          notifications: formData.notifications,
          email_updates: formData.emailUpdates,
          language: 'en'
        }
      }

      if (profile) {
        await userProfileService.updateUserProfile(user.userId, {
          name: formData.name,
          email: formData.email,
          address: formData.address,
          notes: formData.notes,
          preferences
        } as any)
      } else {
        await userProfileService.createUserProfile(
          formData.email,
          formData.name,
          preferences,
          user.userId
        )
      }

      console.log('✅ Profile saved successfully')
      setEditMode(false)
      await loadProfile()
    } catch (error) {
      console.error('❌ Error saving profile:', error)
      setError('Failed to save profile')
    } finally {
      setSaving(false)
    }
  }

  const handleCancel = () => {
    setEditMode(false)
    if (profile && profile.preferences) {
      setFormData({
        name: profile.name || user.username,
        email: profile.email || user.email || '',
        address: profile.address || '',
        notes: (profile as any).notes || '',
        travelBudget: profile.preferences.travel?.budget_range || 'mid-range',
        travelInterests: profile.preferences.travel?.interests || [],
        accommodationType: profile.preferences.travel?.accommodation_type || 'hotels',
        travelStyle: profile.preferences.travel?.travel_style || 'balanced',
        notifications: profile.preferences.communication?.notifications || true,
        emailUpdates: profile.preferences.communication?.email_updates || true,
      })
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-2xl max-w-xl w-[90%] max-h-[90vh] overflow-hidden flex flex-col shadow-2xl">
        <div className="flex justify-between items-center p-4 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-800">User Profile</h2>
          <div className="flex gap-2">
            <button 
              onClick={loadProfile}
              title="Refresh profile"
              className="p-2 text-blue-600 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 10C21 10 18.995 7.26822 17.3662 5.63824C15.7373 4.00827 13.4864 3 11 3C6.02944 3 2 7.02944 2 12C2 16.9706 6.02944 21 11 21C15.1031 21 18.5649 18.2543 19.6482 14.5M21 10V4M21 10H15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
            <button className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors" onClick={onClose}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-6">
          {loading ? (
            <div className="flex flex-col items-center justify-center gap-3 py-12 text-gray-500">
              <div className="loading-spinner"></div>
              <span>Loading profile...</span>
            </div>
          ) : error ? (
            <div className="flex flex-col items-center justify-center gap-3 py-12 text-gray-500">
              <span className="text-3xl">⚠️</span>
              <span>{error}</span>
              <button className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors" onClick={loadProfile}>
                Retry
              </button>
            </div>
          ) : (
            <div className="flex flex-col gap-6">
              {/* Basic Information */}
              <div className="pb-6 border-b border-gray-200">
                <h3 className="text-base font-semibold text-gray-800 mb-4">Basic Information</h3>
                <div className="space-y-4">
                  <div>
                    <label htmlFor="profile-name" className="block text-sm font-medium text-gray-700 mb-1">Display Name</label>
                    <input id="profile-name" type="text" value={formData.name} onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))} disabled={!editMode} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:border-blue-600 disabled:bg-gray-50 disabled:text-gray-500" />
                  </div>
                  <div>
                    <label htmlFor="profile-email" className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                    <input id="profile-email" type="email" value={formData.email} onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))} disabled={!editMode} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:border-blue-600 disabled:bg-gray-50 disabled:text-gray-500" />
                  </div>
                  <div>
                    <label htmlFor="profile-address" className="block text-sm font-medium text-gray-700 mb-1">Address</label>
                    <input id="profile-address" type="text" value={formData.address} onChange={(e) => setFormData(prev => ({ ...prev, address: e.target.value }))} disabled={!editMode} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:border-blue-600 disabled:bg-gray-50 disabled:text-gray-500" />
                  </div>
                  <div>
                    <label htmlFor="profile-notes" className="block text-sm font-medium text-gray-700 mb-1">Notes</label>
                    <textarea id="profile-notes" value={formData.notes} onChange={(e) => setFormData(prev => ({ ...prev, notes: e.target.value }))} disabled={!editMode} rows={4} placeholder="Add any additional notes or preferences..." className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:border-blue-600 disabled:bg-gray-50 disabled:text-gray-500 resize-y" />
                  </div>
                </div>
              </div>

              {/* Travel Preferences */}
              <div className="pb-6 border-b border-gray-200">
                <h3 className="text-base font-semibold text-gray-800 mb-4">Travel Preferences</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Budget Range</label>
                    <select value={formData.travelBudget} onChange={(e) => setFormData(prev => ({ ...prev, travelBudget: e.target.value }))} disabled={!editMode} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:border-blue-600 disabled:bg-gray-50 disabled:text-gray-500">
                      <option value="budget">Budget-friendly</option>
                      <option value="mid-range">Mid-range</option>
                      <option value="luxury">Luxury</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Travel Interests</label>
                    <div className="grid grid-cols-2 gap-2">
                      {travelInterestOptions.map(interest => (
                        <label key={interest} className="flex items-center gap-2 text-sm text-gray-700 cursor-pointer">
                          <input type="checkbox" checked={formData.travelInterests.includes(interest)} onChange={() => handleInterestToggle(interest)} disabled={!editMode} className="rounded" />
                          {interest}
                        </label>
                      ))}
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Accommodation Preference</label>
                    <select value={formData.accommodationType} onChange={(e) => setFormData(prev => ({ ...prev, accommodationType: e.target.value }))} disabled={!editMode} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:border-blue-600 disabled:bg-gray-50 disabled:text-gray-500">
                      <option value="hotels">Hotels</option>
                      <option value="hostels">Hostels</option>
                      <option value="vacation-rentals">Vacation Rentals</option>
                      <option value="mixed">Mixed</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* Communication Preferences */}
              <div className="pb-6">
                <h3 className="text-base font-semibold text-gray-800 mb-4">Communication Preferences</h3>
                <div className="space-y-3">
                  <label className="flex items-center gap-2 text-sm text-gray-700 cursor-pointer">
                    <input type="checkbox" checked={formData.notifications} onChange={(e) => setFormData(prev => ({ ...prev, notifications: e.target.checked }))} disabled={!editMode} className="rounded" />
                    Enable notifications
                  </label>
                  <label className="flex items-center gap-2 text-sm text-gray-700 cursor-pointer">
                    <input type="checkbox" checked={formData.emailUpdates} onChange={(e) => setFormData(prev => ({ ...prev, emailUpdates: e.target.checked }))} disabled={!editMode} className="rounded" />
                    Receive email updates
                  </label>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="flex justify-end gap-3 p-4 border-t border-gray-200">
          {!editMode ? (
            <>
              <button className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-50 transition-colors" onClick={onClose}>
                Close
              </button>
              <button className="px-4 py-2 bg-[#1a1f71] text-white rounded-lg text-sm font-medium" onClick={() => setEditMode(true)}>
                Edit Profile
              </button>
            </>
          ) : (
            <>
              <button className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg text-sm font-medium disabled:opacity-50" onClick={handleCancel} disabled={saving}>
                Cancel
              </button>
              <button className="px-4 py-2 bg-[#1a1f71] text-white rounded-lg text-sm font-medium disabled:opacity-50" onClick={handleSave} disabled={saving || !formData.name.trim()}>
                {saving ? 'Saving...' : 'Save Changes'}
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default UserProfile
