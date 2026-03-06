import { useEffect, useState } from 'react'
import { Amplify } from 'aws-amplify'
import Chat from './components/Chat'
import CartPanel from './components/CartPanel'
import TabbedSidebar from './components/TabbedSidebar'
import UserOnboarding from './components/UserOnboarding'
import UserProfile from './components/UserProfile'
import PurchaseConfirmation from './components/PurchaseConfirmation'
import { useSessions } from './hooks/useSessions'
import { useCart } from './hooks/useCart'
import { ensureUserExists } from './services/userService'
import { userProfileService } from './services/userProfileService'
import { removeCartItems } from './services/cartService'
import { createBooking } from './services/bookingsService'
import outputs from '../../amplify_outputs.json'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import { showToast } from './utils/toast'
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
  const [isCartOpen, setIsCartOpen] = useState(false)
  const [showOnboarding, setShowOnboarding] = useState(false)
  const [showProfile, setShowProfile] = useState(false)
  const [profileLoading, setProfileLoading] = useState(true)
  const [displayName, setDisplayName] = useState<string>(user.username)
  const [currentMessages, setCurrentMessages] = useState<any[]>([])

  const [triggerMessage, setTriggerMessage] = useState<{ message: string; timestamp: number } | undefined>()
  const [showPurchaseFlow, setShowPurchaseFlow] = useState(false)
  const [purchaseCartItems, setPurchaseCartItems] = useState<any[]>([])
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

  const { refreshCartCount } = useCart(user.userId)

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

  const handleToggleCart = () => {
    setIsCartOpen(!isCartOpen)
    if (!isCartOpen) {
      refreshCartCount()
    }
  }

  const handleCloseCart = () => {
    setIsCartOpen(false)
  }

  const handleCartUpdate = () => {
    refreshCartCount()
  }

  const handlePurchaseConfirm = async (cartItems: any[]) => {
    setPurchaseCartItems(cartItems)
    setShowPurchaseFlow(true)
    setIsCartOpen(false)
  }

  const handlePurchaseComplete = async (result: any) => {
    setShowPurchaseFlow(false)

    const orderId = `ORD-${new Date().toISOString().slice(0, 10).replace(/-/g, '')}-${result.instructionId?.slice(-8) || 'XXXX'}`

    if (result.cartItems && result.cartItems.length > 0) {
      for (const item of result.cartItems) {
        await createBooking(user.userId, orderId, {
          item_type: item.item_type || 'product',
          title: item.title,
          price: item.price,
          asin: item.asin,
          url: item.url,
          flight_id: item.details?.flight_id,
          origin: item.details?.origin,
          destination: item.details?.destination,
          departure_date: item.details?.departure_date,
          airline: item.details?.airline,
          hotel_id: item.details?.hotel_id,
          city_code: item.details?.city_code,
          rating: item.details?.rating,
          amenities: item.details?.amenities
        })
      }
      console.log(`📋 Created ${result.cartItems.length} booking records`)
    }

    try {
      const asins: string[] = []
      const flight_ids: string[] = []
      const hotel_ids: string[] = []

      for (const item of result.cartItems) {
        if (item.item_type === 'flight' && item.details?.flight_id) {
          flight_ids.push(item.details.flight_id)
        } else if (item.item_type === 'hotel' && item.details?.hotel_id) {
          hotel_ids.push(item.details.hotel_id)
        } else if (item.asin) {
          asins.push(item.asin)
        }
      }

      await removeCartItems(user.userId, { asins, flight_ids, hotel_ids })
    } catch (error) {
      console.error('Error removing purchased items from cart:', error)
    }

    setTriggerMessage({
      message: `Purchase completed successfully! Payment authorized for $${result.totalAmount}. Order ID: ${orderId}`,
      timestamp: Date.now()
    })

    refreshCartCount()
    setRefreshTrigger(Date.now())
  }

  const handlePurchaseError = (error: string) => {
    setShowPurchaseFlow(false)
    showToast.error(`Purchase failed: ${error}. Please try again or contact support.`)
  }

  const handlePurchaseCancel = () => {
    setShowPurchaseFlow(false)
  }

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
            <img src="/VISA-Logo-2006.png" alt="Visa" className="h-8" />
            <h1 className="text-xl font-semibold text-[#0a3a7a]">Concierge Agent</h1>
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

      {showPurchaseFlow && (
        <PurchaseConfirmation
          userEmail={user.email || `${user.username}@example.com`}
          userId={user.userId}
          cartItems={purchaseCartItems}
          onComplete={handlePurchaseComplete}
          onError={handlePurchaseError}
          onCancel={handlePurchaseCancel}
        />
      )}

      {/* Header */}
      <header className="bg-[#1a1f71] text-white px-6 py-3 flex items-center justify-between z-10">
        <div className="flex items-center gap-3">
          <img src="/VISA-Logo-2006.png" alt="Visa" className="h-8" />
          <h1 className="text-xl font-semibold">Concierge Agent</h1>
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
          
          <button 
            onClick={handleToggleCart}
            className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              isCartOpen ? 'bg-white text-[#0a3a7a]' : 'text-white/90 hover:bg-white/10'
            }`}
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M3 3H5L5.4 5M7 13H17L21 5H5.4M7 13L5.4 5M7 13L4.7 15.3C4.3 15.7 4.6 16.5 5.1 16.5H17M17 13V16.5M9 19.5A1.5 1.5 0 1 0 9 22.5A1.5 1.5 0 0 0 9 19.5ZM20 19.5A1.5 1.5 0 1 0 20 22.5A1.5 1.5 0 0 0 20 19.5Z"/>
            </svg>
            {isCartOpen ? 'Close Cart' : 'View Cart'}
          </button>
        </div>
      </header>
      
      <CartPanel
        user={user}
        isOpen={isCartOpen}
        onClose={handleCloseCart}
        onCartUpdate={handleCartUpdate}
        onPurchaseConfirm={handlePurchaseConfirm}
        refreshTrigger={refreshTrigger}
      />
      
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
          onCartUpdate={handleCartUpdate}
        />
        <TabbedSidebar user={user} messages={currentMessages} refreshTrigger={refreshTrigger} />
      </div>
    </div>
  )
}

function App() {
  const [ready, setReady] = useState(false)

  useEffect(() => {
    // Ensure demo user record exists for data layer, then render
    ensureUserExists(DEMO_USER.userId)
      .then(() => setReady(true))
      .catch((err) => {
        console.warn('Could not ensure demo user exists (data layer may be unavailable):', err)
        setReady(true) // proceed anyway
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
