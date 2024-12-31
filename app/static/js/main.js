// MSAL Authentication
async function signIn() {
    try {
        // Define login request
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

        // Check if there's a cached account
        const accounts = msalInstance.getAllAccounts();
        if (accounts.length > 0) {
            // Use the first account if available
            const silentRequest = {
                scopes: loginRequest.scopes,
                account: accounts[0],
                forceRefresh: false
            };

            try {
                const response = await msalInstance.acquireTokenSilent(silentRequest);
                await handleTokenResponse(response);
                return;
            } catch (error) {
                if (error instanceof msal.InteractionRequiredAuthError) {
                    // Fall back to interaction when silent call fails
                    await performInteractiveSignIn(loginRequest);
                }
            }
        } else {
            // No accounts, perform interactive sign in
            await performInteractiveSignIn(loginRequest);
        }
    } catch (error) {
        console.error('Error during sign in:', error);
    }
}

async function performInteractiveSignIn(loginRequest) {
    try {
        const response = await msalInstance.loginPopup(loginRequest);
        await handleTokenResponse(response);
    } catch (error) {
        console.error('Error during interactive sign in:', error);
    }
}

async function handleTokenResponse(response) {
    try {
        // Send token to backend
        const backendResponse = await fetch('/auth/callback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                token: response.accessToken,
                account: response.account
            })
        });

        if (backendResponse.ok) {
            const data = await backendResponse.json();
            if (data.redirect) {
                window.location.href = data.redirect;
            } else {
                window.location.href = '/dashboard';
            }
        } else {
            throw new Error('Backend authentication failed');
        }
    } catch (error) {
        console.error('Error handling token response:', error);
    }
}

async function signOut() {
    try {
        const account = msalInstance.getAllAccounts()[0];
        if (account) {
            await msalInstance.logoutPopup({
                account: account,
                postLogoutRedirectUri: window.location.origin
            });

            // Clear session storage
            sessionStorage.clear();

            // Redirect to logout endpoint
            window.location.href = '/auth/logout';
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