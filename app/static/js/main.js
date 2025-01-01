// MSAL Authentication
async function signIn() {
    const loginRequest = {
        scopes: [
            "https://graph.microsoft.com/Calendars.Read",
            "https://graph.microsoft.com/User.Read",
            "https://graph.microsoft.com/OnlineMeetings.Read",
            "offline_access",
            "openid",
            "profile",
            "email"
        ]
    };

    try {
        // Clear any existing state before proceeding
        sessionStorage.clear();
        localStorage.clear();

        // Proceed with login
        await msalInstance.loginRedirect(loginRequest);
    } catch (error) {
        console.error('Error during sign in:', error);
        if (error.errorCode === "interaction_in_progress") {
            window.location.reload();
        }
    }
}

async function signOut() {
    try {
        // Get MSAL instance and accounts first
        const msalInstance = new msal.PublicClientApplication(msalConfig);
        const accounts = msalInstance.getAllAccounts();

        // Clear all browser storage
        sessionStorage.clear();
        localStorage.clear();
        
        // Clear all cookies
        document.cookie.split(";").forEach(function(c) { 
            document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); 
        });

        // Sign out from MSAL first if there are accounts
        if (accounts.length > 0) {
            try {
                // Clear MSAL cache for all accounts
                accounts.forEach(account => {
                    msalInstance.clearCache(account);
                });

                // Perform MSAL logout
                await msalInstance.logoutPopup({
                    account: accounts[0],
                    mainWindowRedirectUri: window.location.origin + '/auth/auth-start'
                });
            } catch (msalError) {
                console.error('MSAL logout error:', msalError);
            }
        }

        // Then sign out from our backend
        try {
            const response = await fetch('/auth/logout', {
                method: 'GET',
                headers: {
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error('Backend logout failed');
            }
        } catch (backendError) {
            console.error('Backend logout error:', backendError);
        }

        // Final cleanup and redirect
        sessionStorage.clear();
        localStorage.clear();
        window.location.href = '/auth/auth-start';
    } catch (error) {
        console.error('Error during sign out:', error);
        // Force redirect to login page on error
        window.location.href = '/auth/auth-start';
    }
}

// Dashboard Functions
async function startSync() {
    try {
        const response = await fetch('/api/sync', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error('Sync failed');
        }
        
        window.location.reload();
    } catch (error) {
        console.error('Error during sync:', error);
    }
}

async function matchTask(meetingId) {
    try {
        const response = await fetch(`/api/meetings/${meetingId}/match`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error('Task matching failed');
        }
        
        window.location.reload();
    } catch (error) {
        console.error('Error matching task:', error);
    }
}

async function postAllMatched() {
    try {
        const response = await fetch('/api/meetings/post-all', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error('Posting matched meetings failed');
        }
        
        window.location.reload();
    } catch (error) {
        console.error('Error posting matched meetings:', error);
    }
}

// Check authentication state on page load
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const accounts = msalInstance.getAllAccounts();
        const currentPath = window.location.pathname;
        
        if (accounts.length > 0 && currentPath === '/') {
            // We have an account but we're on the login page
            // Try silent token acquisition
            const silentRequest = {
                scopes: ["https://graph.microsoft.com/User.Read"],
                account: accounts[0],
                forceRefresh: false
            };
            
            try {
                const response = await msalInstance.acquireTokenSilent(silentRequest);
                if (response) {
                    window.location.href = '/dashboard';
                }
            } catch (error) {
                if (error instanceof msal.InteractionRequiredAuthError) {
                    // Token expired or other issue, stay on login page
                    console.log('Silent token acquisition failed, user needs to sign in');
                }
            }
        }
    } catch (error) {
        console.error('Error checking authentication state:', error);
    }
});

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Check if we have a stored account
    const account = msalInstance.getAllAccounts()[0];
    if (account) {
        // Update UI to show logged in state
        console.log('User is signed in:', account.username);
    }

    // Handle Start Sync button
    const syncButton = document.querySelector('[data-action="sync"]');
    if (syncButton) {
        syncButton.addEventListener('click', startSync);
    }
    
    // Handle Match Task buttons
    const matchButtons = document.querySelectorAll('[data-action="match"]');
    matchButtons.forEach(button => {
        button.addEventListener('click', () => {
            const meetingId = button.dataset.meetingId;
            matchTask(meetingId);
        });
    });
    
    // Handle Post All button
    const postAllButton = document.querySelector('[data-action="post-all"]');
    if (postAllButton) {
        postAllButton.addEventListener('click', postAllMatched);
    }

    // Prevent back button from returning to dashboard after logout
    window.addEventListener('pageshow', function(event) {
        if (event.persisted) {
            // Page was loaded from cache (back button)
            window.location.reload();
        }
    });

    // Prevent caching of dashboard page
    if (window.location.pathname.startsWith('/dashboard')) {
        if (window.performance && window.performance.navigation.type === window.performance.navigation.TYPE_BACK_FORWARD) {
            window.location.reload();
        }
    }
}); 