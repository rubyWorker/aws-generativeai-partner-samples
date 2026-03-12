import { useEffect, useState } from 'react'
import { Amplify } from 'aws-amplify'
import Chat from './components/Chat'
import TabbedSidebar from './components/TabbedSidebar'
import UserOnboarding from './components/UserOnboarding'
import UserProfile from './components/UserProfile'
import { useSessions } from './hooks/useSessions'
import { ensureUserExists } from './services/userService'
import { userProfileService } from './services/userProfileService'
import outputs from '../../amplify_outputs.json'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import './styles/travel-theme.css'

// Configure Amplify for data layer (AppSync) only — auth disabled
Amplify.configure(outputs)

interface User {
  username: string
  email?: string
  userId: string
  name?: string
}

// Demo user — no login required
const DEMO_USER: User = {
  username: 'Demo User',
  email: 'demo@example.com',
  userId: 'demo-user',
  name: 'Demo User',
}

interface AppWithSessionsProps {
  user: User
}

const AppWithSessions = ({ user }: AppWithSessionsProps) => {
  const [showOnboarding, setShowOnboarding] = useState(false)
  const [showProfile, setShowProfile] = useState(false)
  const [profileLoading, setProfileLoading] = useState(true)
  const [displayName, setDisplayName] = useState<string>(user.username)
  const [currentMessages, setCurrentMessages] = useState<any[]>([])

  const [triggerMessage, setTriggerMessage] = useState<{ message: string; timestamp: number } | undefined>()
  const [refreshTrigger, setRefreshTrigger] = useState<number>(0)
  
  const {
    sessions,
    currentSession,
    loading,
    error,
    switchToSession,
    startNewConversation,
    getMessages,
    refreshSessions,
    updateCurrentSession
  } = useSessions(user.userId)

  // Load messages when session changes
  useEffect(() => {
    if (currentSession) {
      getMessages(currentSession.id).then(messages => {
        setCurrentMessages(messages)
      })
    } else {
      setCurrentMessages([])
    }
  }, [currentSession, getMessages])

  // Check if user needs onboarding and get display name
  useEffect(() => {
    const checkUserProfile = async () => {
      try {
        const profile = await userProfileService.getUserProfile(user.userId)
        if (!profile || !profile.onboardingCompleted) {
          setShowOnboarding(true)
        }
        if (profile && profile.name) {
          setDisplayName(profile.name)
        }
      } catch (error) {
        console.error('Error checking user profile:', error)
        setShowOnboarding(true)
      } finally {
        setProfileLoading(false)
      }
    }

    checkUserProfile()
  }, [user.userId])

  const handleOnboardingComplete = () => {
    setShowOnboarding(false)
    userProfileService.getUserProfile(user.userId)
      .then(profile => {
        if (profile && profile.name) {
          setDisplayName(profile.name)
        }
      })
      .catch(() => { /* Profile refresh failed silently */ })
  }

  if (profileLoading) {
    return (
      <div className="flex flex-col h-screen">
        <header className="bg-white text-gray-800 px-6 py-4 flex items-center justify-between border-b border-gray-200">
          <div className="flex items-center gap-3">
            <h1 className="text-xl font-semibold text-[#0a3a7a]">Travel Concierge Agent</h1>
          </div>
        </header>
        <div className="flex-1 flex flex-col items-center justify-center gap-4 text-white">
          <div className="loading-spinner"></div>
          <div>Setting up your profile...</div>
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-screen overflow-hidden">
      <ToastContainer />

      {showOnboarding && (
        <UserOnboarding user={user} onComplete={handleOnboardingComplete} />
      )}
      
      <UserProfile user={user} isOpen={showProfile} onClose={() => setShowProfile(false)} />

      {/* Header */}
      <header className="bg-[#1a1f71] text-white px-6 py-3 flex items-center justify-between z-10">
        <div className="flex items-center gap-3">
          <h1 className="text-xl font-semibold">Travel Concierge Agent</h1>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-sm text-white/80">Welcome, {displayName}!</span>

          <button
            onClick={() => setShowProfile(true)}
            className="flex items-center gap-2 px-3 py-2 text-white/90 hover:bg-white/10 rounded-lg text-sm font-medium transition-colors"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
            Profile
          </button>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden">
        <Chat
          user={user}
          onSignOut={() => {}}
          currentSession={currentSession}
          sessions={sessions}
          onSwitchSession={(sessionId) => {
            const session = sessions.find(s => s.id === sessionId)
            if (session) switchToSession(session)
          }}
          getMessages={getMessages}
          refreshSessions={refreshSessions}
          updateCurrentSession={updateCurrentSession}
          onMessagesUpdate={setCurrentMessages}
          triggerMessage={triggerMessage}
          onNewChat={startNewConversation}
          canStartNewChat={!loading}
        />
        <TabbedSidebar user={user} messages={currentMessages} refreshTrigger={refreshTrigger} />
      </div>
    </div>
  )
}

function App() {
  const [ready, setReady] = useState(false)

  useEffect(() => {
    ensureUserExists(DEMO_USER.userId)
      .then(() => setReady(true))
      .catch((err) => {
        console.warn('Could not ensure demo user exists (data layer may be unavailable):', err)
        setReady(true)
      })
  }, [])

  if (!ready) {
    return (
      <div className="App" style={{ padding: '2rem', textAlign: 'center' }}>
        <div>Loading...</div>
      </div>
    )
  }

  return (
    <div className="App">
      <AppWithSessions user={DEMO_USER} />
    </div>
  )
}

export default App
