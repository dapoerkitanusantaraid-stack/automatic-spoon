/**
 * Project Server Mobile SDK
 * Untuk mengumpulkan data customer dari perangkat mereka
 * 
 * Usage:
 * <script src="https://yourdomain.com/sdk.js"></script>
 * <script>
 *   ProjectServerSDK.init({
 *     apiBase: 'https://api.yourdomain.com',
 *     trackingEnabled: true
 *   });
 * </script>
 */

class ProjectServerSDK {
    constructor() {
        this.apiBase = 'http://localhost:8000';
        this.customerId = null;
        this.sessionId = this.generateSessionId();
        this.trackingEnabled = true;
        this.deviceInfo = {};
        this.userData = {};
    }

    /**
     * Initialize SDK
     */
    static init(config = {}) {
        const sdk = new ProjectServerSDK();
        
        if (config.apiBase) sdk.apiBase = config.apiBase;
        if (config.trackingEnabled !== undefined) sdk.trackingEnabled = config.trackingEnabled;
        
        // Collect device info
        sdk.collectDeviceInfo();
        
        // Setup event listeners
        sdk.setupEventListeners();
        
        // Store in window
        window.ProjectServerSDK = sdk;
        
        console.log('✅ ProjectServerSDK initialized');
        return sdk;
    }

    /**
     * Collect device information
     */
    collectDeviceInfo() {
        this.deviceInfo = {
            userAgent: navigator.userAgent,
            language: navigator.language,
            platform: navigator.platform,
            screenResolution: `${window.screen.width}x${window.screen.height}`,
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            localStorage: typeof(Storage) !== "undefined",
            cookies: navigator.cookieEnabled,
            timestamp: new Date().toISOString(),
            device: this.detectDevice(),
            browser: this.detectBrowser()
        };
    }

    /**
     * Detect device type
     */
    detectDevice() {
        const ua = navigator.userAgent;
        if (/Android/i.test(ua)) {
            return {
                platform: 'Android',
                type: 'mobile'
            };
        }
        if (/iPhone|iPad|iPod/i.test(ua)) {
            return {
                platform: 'iOS',
                type: 'mobile'
            };
        }
        return {
            platform: 'Desktop',
            type: 'computer'
        };
    }

    /**
     * Detect browser
     */
    detectBrowser() {
        const ua = navigator.userAgent;
        let browser = 'Unknown';
        
        if (ua.indexOf('Firefox') > -1) browser = 'Firefox';
        else if (ua.indexOf('Chrome') > -1) browser = 'Chrome';
        else if (ua.indexOf('Safari') > -1) browser = 'Safari';
        else if (ua.indexOf('Edge') > -1) browser = 'Edge';
        
        return browser;
    }

    /**
     * Generate unique session ID
     */
    generateSessionId() {
        return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Register customer
     */
    async registerCustomer(userData = {}) {
        try {
            const data = {
                nama: userData.nama || 'Guest',
                email: userData.email || '',
                phone: userData.phone || this.getPhoneFromStorage(),
                sumber: 'web',
                device_info: this.deviceInfo,
                metadata: {
                    sessionId: this.sessionId,
                    ...userData.metadata
                }
            };

            const response = await fetch(`${this.apiBase}/customer/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                const result = await response.json();
                this.customerId = result.customer_id;
                this.userData = userData;
                
                // Store customer ID locally
                localStorage.setItem('project_server_customer_id', this.customerId);
                
                console.log('✅ Customer registered:', this.customerId);
                return result;
            } else {
                console.error('❌ Failed to register customer');
                return null;
            }
        } catch (error) {
            console.error('Error registering customer:', error);
            return null;
        }
    }

    /**
     * Log user interaction
     */
    async logInteraction(action, kontenId = null) {
        if (!this.trackingEnabled || !this.customerId) return;

        try {
            const data = {
                platform: 'web',
                action: action,
                konten_id: kontenId,
                timestamp: new Date().toISOString()
            };

            await fetch(`${this.apiBase}/customer/${this.customerId}/log`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            console.log(`📊 Interaction logged: ${action}`);
        } catch (error) {
            console.error('Error logging interaction:', error);
        }
    }

    /**
     * Track konten view
     */
    async trackKontenView(kontenId) {
        await this.logInteraction('view_konten', kontenId);
    }

    /**
     * Track galeri view
     */
    async trackGaleriView(kontenId) {
        await this.logInteraction('view_galeri', kontenId);
    }

    /**
     * Track link click
     */
    async trackLinkClick(kontenId) {
        await this.logInteraction('click_link', kontenId);
    }

    /**
     * Setup automatic event listeners
     */
    setupEventListeners() {
        // Track page view
        window.addEventListener('load', () => {
            this.logInteraction('page_load');
        });

        // Track time on page
        const unloadHandler = () => {
            this.logInteraction('page_unload');
        };
        window.addEventListener('beforeunload', unloadHandler);

        // Track link clicks dengan data-track attribute
        document.addEventListener('click', (e) => {
            const link = e.target.closest('[data-track="true"]');
            if (link) {
                const kontenId = link.getAttribute('data-konten-id');
                this.trackLinkClick(kontenId);
            }
        });
    }

    /**
     * Get phone from storage atau prompt user
     */
    getPhoneFromStorage() {
        return localStorage.getItem('user_phone') || '';
    }

    /**
     * Set user phone
     */
    setUserPhone(phone) {
        localStorage.setItem('user_phone', phone);
    }

    /**
     * Request device permission (contacts, location, etc)
     */
    async requestPermissions() {
        const permissions = {
            contacts: false,
            location: false,
            camera: false,
            microphone: false
        };

        // Request Geolocation
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    permissions.location = true;
                    this.deviceInfo.location = {
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude,
                        accuracy: position.coords.accuracy
                    };
                },
                (error) => console.log('Location access denied')
            );
        }

        // Note: Contacts, Camera, Microphone memerlukan user interaction
        // dan HTTPS connection untuk beberapa browser

        return permissions;
    }

    /**
     * Share data (untuk social sharing)
     */
    async shareKonten(konten) {
        if (navigator.share) {
            try {
                await navigator.share({
                    title: konten.judul,
                    text: konten.deskripsi,
                    url: `https://yourdomain.com/?konten=${konten.id}`
                });
                this.logInteraction('share_konten', konten.id);
            } catch (error) {
                console.log('Share cancelled:', error);
            }
        } else {
            console.log('Web Share API not supported');
            // Fallback: copy link to clipboard
            const link = `https://yourdomain.com/?konten=${konten.id}`;
            navigator.clipboard.writeText(link);
            alert('Link copied to clipboard!');
        }
    }

    /**
     * Get customer info
     */
    getCustomerInfo() {
        return {
            customerId: this.customerId,
            sessionId: this.sessionId,
            userData: this.userData,
            deviceInfo: this.deviceInfo
        };
    }

    /**
     * Sync all data
     */
    async syncData() {
        if (this.customerId) {
            console.log('🔄 Syncing data with server...');
            await this.registerCustomer(this.userData);
        }
    }
}

// Export untuk module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ProjectServerSDK;
}
