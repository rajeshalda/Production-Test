// MSAL Authentication
async function signIn() {
    try {
        // Define login request
        const loginRequest = {
            scopes: [
                "https://graph.microsoft.com/Calendars.Read",
                "https://graph.microsoft.com/User.Read",
                "https://graph.microsoft.com/OnlineMeetings.Read"
            ],
            prompt: 'select_account'
        };

        // Clear any existing accounts
        const accounts = msalInstance.getAllAccounts();
        if (accounts.length > 0) {
            accounts.forEach(account => {
                msalInstance.logoutRedirect({ account });
            });
        }

        // Use popup for login
        const response = await msalInstance.loginPopup(loginRequest);
        console.log("Login successful", response);

        // Get token using silent flow
        const silentRequest = {
            scopes: loginRequest.scopes,
            account: response.account,
            forceRefresh: true
        };

        const tokenResponse = await msalInstance.acquireTokenSilent(silentRequest);
        console.log("Token acquired", tokenResponse);

        // Send token to backend
        const backendResponse = await fetch('/auth/callback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                token: tokenResponse.accessToken,
                account: response.account
            })
        });

        if (backendResponse.ok) {
            window.location.href = '/dashboard';
        } else {
            throw new Error('Backend authentication failed');
        }
    } catch (error) {
        console.error('Error during sign in:', error);
        if (error instanceof msal.InteractionRequiredAuthError) {
            try {
                // Fallback to interactive method
                const response = await msalInstance.acquireTokenPopup(loginRequest);
                console.log("Token acquired through popup", response);
                window.location.href = '/dashboard';
            } catch (err) {
                console.error('Error during interactive token acquisition:', err);
            }
        }
    }
}

async function signOut() {
    try {
        const account = msalInstance.getAllAccounts()[0];
        if (account) {
            // Clear browser state
            await msalInstance.logoutPopup({
                account: account,
                postLogoutRedirectUri: window.location.origin
            });

            // Clear local storage
            localStorage.clear();
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