export interface CognitoUserInfo {
  userId: string
  email?: string
  givenName?: string
  familyName?: string
  fullName?: string
}

/**
 * Return static user info — Cognito auth removed.
 */
export const getCognitoUserInfo = async (userId: string): Promise<CognitoUserInfo> => ({
  userId,
  fullName: 'Demo User',
  email: 'demo@example.com',
})

/**
 * Get display name for the user
 */
export const getDisplayName = (userInfo: CognitoUserInfo): string => {
  return userInfo.fullName || userInfo.givenName || userInfo.email?.split('@')[0] || userInfo.userId
}
