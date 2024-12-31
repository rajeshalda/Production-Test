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
        // Check for existing session
        const accounts = msalInstance.getAllAccounts();
        if (accounts.length > 0) {
            // Try silent token acquisition
            try {
                const silentRequest = {
                    scopes: loginRequest.scopes,
                    account: accounts[0]
                };
                const response = await msalInstance.acquireTokenSilent(silentRequest);
                if (response) {
                    window.location.href = '/dashboard';
                    return;
                }
            } catch (error) {
                if (error instanceof msal.InteractionRequiredAuthError) {
                    // Token expired or other issue, proceed with login
                    console.log('Silent token acquisition failed, proceeding with redirect');
                }
            }
        }

        // Clear any existing state before proceeding
        sessionStorage.clear();

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
        const account = msalInstance.getAllAccounts()[0];
        if (account) {
            await msalInstance.logoutRedirect({
                account: account,
                postLogoutRedirectUri: window.location.origin
            });
        }
    } catch (error) {
        console.error('Error during sign out:', error);
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
}); 