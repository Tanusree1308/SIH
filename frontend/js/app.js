// NO IMPORT STATEMENT AT THE TOP

// --- CONFIGURATION ---
const API_BASE_URL ='https://sih-pp45.onrender.com';

// --- TRANSLATIONS ---
const translations = {
    en: {
        selectLanguageTitle: "Select Language", selectLanguageSubtitle: "Choose your preferred language to continue.", loginTitle: "Welcome Back!", loginSubtitle: "Log in to continue to Bovilens.", usernamePlaceholder: "Username", passwordPlaceholder: "Password", loginButton: "LOGIN", notRegistered: "Not registered?", createAccountLink: "Create an account", registerTitle: "Create Your Account", registerSubtitle: "Get started with Bovilens.", namePlaceholder: "Name", emailPlaceholder: "Email Address", agePlaceholder: "Age", phonePlaceholder: "Phone Number", confirmPasswordPlaceholder: "Confirm Password", registerButton: "REGISTER", alreadyAccount: "Already have an account?", loginHereLink: "Login here", dashboard: "Dashboard", uploadPhoto: "Upload Photo", uploadSubtitleShort: "Select from your gallery", scanPhoto: "Scan Photo", scanSubtitleShort: "Use your camera directly", userProfile: "User Profile", profileSettings: "Settings", uploadTitle: "Upload Photo", uploadSubtitle: "Select an image from your gallery.", previewText: "Image preview will appear here", selectImageBtn: "Select Image", submitScanBtn: "Submit for Analysis", scanningTitle: "Scan Animal", scanningSubtitle: "Position the animal and capture.", analyzingTitle: "Analyzing...", analyzingSubtitle: "Extracting features and calculating the score.", resultsTitle: "Results", resultsSubtitle: "Here is the ATC score for your animal.", annotatedImagePlaceholder: "Annotated image will be here", overallScoreLabel: "Overall Score", menu: "Menu", securityAndPrivacy: "Security & Privacy", helpAndSupport: "Help & Support", signOut: "Sign Out", editPersonalInfo: "Edit Personal Information", additionalFeatures: "Additional User Features", saveChanges: "Save Changes", currentPassword: "Current Password", newPassword: "New Password", confirmNewPassword: "Confirm New Password", changePassword: "Change Password", faqs: "FAQs", userGuide: "User Guide", contactSupport: "Contact Support", privacyPolicy: "Privacy Policy", termsOfService: "Terms of Service", appVersion: "App Version 1.0.0", loginHeader: "Log In", loginUsernameLabel: "Username", loginPasswordLabel: "Password", loginSubmitLabel: "Log In", loginSwitchPrompt: "Don't have an account?", loginSwitchLink: "Sign Up", viewMoreDetails: "View More Details", traitScoresTitle: "Trait Scores", traitBodyLength: "Body Length:", traitWithersHeight: "Withers Height:", traitHipHeight: "Hip Height:", traitChestDepth: "Chest Depth:", traitBodyWidth: "Body Width:", retakeButton: "Retake", submitButton: "Submit", faqTitle: "Frequently Asked Questions", faqQ1: "What is Bovilens?", faqA1: "Bovilens is a mobile app that uses Artificial Intelligence (AI) to analyze the physical traits of your cattle through your phone's camera. It gives you an instant \"ATC Score\" to help you quickly assess an animal's body conformation and quality.", faqQ2: "Who is this app for?", faqA2: "This app is designed for dairy farmers, cattle breeders, livestock traders, and veterinary professionals who want a quick and modern way to evaluate cattle.", faqQ3: "What is the \"ATC Score\"?", faqA3: "The ATC (Animal Trait Conformation) Score is a rating from 1 to 5 based on key physical traits like body length, withers height, and chest depth. A higher score generally indicates better physical structure and conformation according to standard breeding principles.", faqQ4: "How do I take the best photo for an accurate score?", faqA4: "For the most accurate results, make sure the animal is standing on flat, level ground. Take the photo from the side, capturing the entire body from head to tail. Ensure there is good, clear daylight, avoiding dark shadows.", faqQ5: "Is the score 100% accurate?", faqA5: "Our AI is trained on thousands of animal images to be very accurate. However, the score should be used as a reference tool to aid your judgment. It is always best to use it along with your own experience and the advice of a veterinarian.", faqQ6: "Do I need an internet connection to use the app?", faqA6: "Yes. You need an active internet connection (either Wi-Fi or mobile data) when you submit a photo. The analysis is a complex process that happens on our secure servers.",
    },
    hi: {
        selectLanguageTitle: "भाषा चुनें", selectLanguageSubtitle: "जारी रखने के लिए अपनी पसंदीदा भाषा चुनें।", loginTitle: "वापसी पर स्वागत है!", loginSubtitle: "Bovilens पर जारी रखने के لیے लॉग इन करें।", usernamePlaceholder: "उपयोगकर्ता नाम", passwordPlaceholder: "पासवर्ड", loginButton: "लॉग इन करें", notRegistered: "पंजीकृत नहीं हैं?", createAccountLink: "खाता बनाएं", registerTitle: "अपना खाता बनाएं", registerSubtitle: "Bovilens के साथ शुरुआत करें।", namePlaceholder: "नाम", emailPlaceholder: "ईमेल पता", agePlaceholder: "उम्र", phonePlaceholder: "फ़ोन नंबर", confirmPasswordPlaceholder: "पासवर्ड की पुष्टि कीजिये", registerButton: "पंजीकरण करें", alreadyAccount: "पहले से ही एक खाता है?", loginHereLink: "यहां लॉगिन करें", dashboard: "डैशबोर्ड", uploadPhoto: "तस्वीर डालें", uploadSubtitleShort: "अपनी गैलरी से चुनें", scanPhoto: "फोटो स्कैन करें", scanSubtitleShort: "सीधे ਆਪਣੇ कैमरे का उपयोग करें", userProfile: "उपयोगकर्ता प्रोफ़ाइल", profileSettings: "सेटिंग्स", uploadTitle: "तस्वीर डालें", uploadSubtitle: "अपनी गैलरी से एक छवि चुनें।", previewText: "छवि पूर्वावलोकन यहाँ दिखाई देगा", selectImageBtn: "छवि चुनें", submitScanBtn: "विश्लेषण के लिए सबमिट करें", scanningTitle: "जानवर को स्कैन करें", scanningSubtitle: "जानवर को फ्रेम में रखकर फोटो खींचें।", analyzingTitle: "विश्लेषण हो रहा है...", analyzingSubtitle: "विशेषताएँ निकाली जा रही हैं और स्कोर की गणना की जा रही है।", resultsTitle: "परिणाम", resultsSubtitle: "यहाँ आपके पशु का एटीसी स्कोर है।", annotatedImagePlaceholder: "एनोटेट की गई छवि यहाँ होगी", overallScoreLabel: "कुल स्कोर", menu: "मेन्यू", securityAndPrivacy: "सुरक्षा और गोपनीयता", helpAndSupport: "सहायता और समर्थन", signOut: "साइन आउट", editPersonalInfo: "व्यक्तिगत जानकारी संपादित करें", additionalFeatures: "अतिरिक्त उपयोगकर्ता सुविधाएँ", saveChanges: "बदलाव सहेजें", currentPassword: "वर्तमान पासवर्ड", newPassword: "नया पासवर्ड", confirmNewPassword: "नए पासवर्ड की पुष्टि करें", changePassword: "पासवर्ड बदलें", faqs: "पूछे जाने वाले प्रश्न", userGuide: "उपयोगकर्ता गाइड", contactSupport: "सहायता से संपर्क करें", privacyPolicy: "गोपनीयता नीति", termsOfService: "सेवा की शर्तें", appVersion: "ऐप संस्करण 1.0.0", loginHeader: "लॉग इन करें", loginUsernameLabel: "उपयोगकर्ता नाम", loginPasswordLabel: "पासवर्ड", loginSubmitLabel: "लॉग इन करें", loginSwitchPrompt: "खाता नहीं है?", loginSwitchLink: "साइन अप करें", viewMoreDetails: "और विवरण देखें", traitScoresTitle: "गुण स्कोर", traitBodyLength: "शरीर की लंबाई:", traitWithersHeight: "कंधे की ऊंचाई:", traitHipHeight: "कूल्हे की ऊंचाई:", traitChestDepth: "छाती की गहराई:", traitBodyWidth: "शरीर की चौड़ाई:", retakeButton: "फिर से लें", submitButton: "सबमिट करें", faqTitle: "अक्सर पूछे जाने वाले प्रश्न", faqQ1: "बोविलेंस क्या है?", faqA1: "बोविलेंस एक मोबाइल ऐप है जो आर्टिफिशियल इंटेलिजेंस (एआई) का उपयोग करके आपके फोन के कैमरे से आपके मवेशियों के शारीरिक लक्षणों का विश्लेषण करता है। यह आपको जानवर के शरीर की बनावट और गुणवत्ता का तुरंत आकलन करने में मदद करने के लिए एक तत्काल \"एटीसी स्कोर\" देता है।", faqQ2: "यह ऐप किसके लिए है?", faqA2: "यह ऐप डेयरी किसानों, मवेशी प्रजनकों, पशु व्यापारियों और पशु चिकित्सा पेशेवरों के लिए डिज़ाइन किया गया है जो मवेशियों का मूल्यांकन करने का एक त्वरित और आधुनिक तरीका चाहते हैं।", faqQ3: "\"एटीसी स्कोर\" क्या है?", faqA3: "एटीसी (पशु लक्षण रचना) स्कोर शरीर की लंबाई, कंधों की ऊंचाई और छाती की गहराई जैसे प्रमुख शारीरिक लक्षणों के आधार पर 1 से 5 तक की रेटिंग है। एक उच्च स्कोर आम तौर पर मानक प्रजनन सिद्धांतों के अनुसार बेहतर शारीरिक संरचना और बनावट को इंगित करता है।", faqQ4: "सटीक स्कोर के लिए सबसे अच्छी तस्वीर कैसे लें?", faqA4: "सबसे सटीक परिणामों के लिए, सुनिश्चित करें कि जानवर समतल जमीन पर खड़ा है। तस्वीर बगल से लें, जिसमें सिर से पूंछ तक पूरा शरीर दिखाई दे। सुनिश्चित करें कि दिन की रोशनी अच्छी और साफ हो, और गहरी छाया से बचें।", faqQ5: "क्या स्कोर 100% सटीक है?", faqA5: "हमारे एआई को बहुत सटीक होने के लिए हजारों जानवरों की छवियों पर प्रशिक्षित किया गया है। हालांकि, स्कोर का उपयोग आपके निर्णय में सहायता के लिए एक संदर्भ उपकरण के रूप में किया जाना चाहिए। इसे हमेशा अपने अनुभव और पशुचिकित्सक की सलाह के साथ उपयोग करना सबसे अच्छा है।", faqQ6: "क्या मुझे ऐप का उपयोग करने के लिए इंटरनेट कनेक्शन की आवश्यकता है?", faqA6: "हाँ। फोटो सबमिट करते समय आपको एक सक्रिय इंटरनेट कनेक्शन (या तो वाई-फाई या मोबाइल डेटा) की आवश्यकता होती है। विश्लेषण एक जटिल प्रक्रिया है जो हमारे सुरक्षित सर्वर पर होती है।",
    },
    te: {
        selectLanguageTitle: "భాషను ఎంచుకోండి", selectLanguageSubtitle: "కొనసాగించడానికి మీకు ఇష్టమైన భాషను ఎంచుకోండి.", loginTitle: " తిరిగి స్వాగతం!", loginSubtitle: "Bovilensకు కొనసాగడానికి లాగిన్ చేయండి.", usernamePlaceholder: "వినియోగదారు పేరు", passwordPlaceholder: "పాస్వర్డ్", loginButton: "లాగిన్ చేయండి", notRegistered: "నమోదు కాలేదా?", createAccountLink: "ఖాతా సృష్టించండి", registerTitle: "మీ ఖాతాను సృష్టించండి", registerSubtitle: "Bovilensతో ప్రారంభించండి.", namePlaceholder: "పేరు", emailPlaceholder: "ఇమెయిల్ చిరునామా", agePlaceholder: "వయస్సు", phonePlaceholder: "ఫోన్ నంబర్", confirmPasswordPlaceholder: "పాస్వర్డ్ను నిర్ధారించండి", registerButton: "నమోదు చేసుకోండి", alreadyAccount: "ఇప్పటికే ఖాతా ఉందా?", loginHereLink: "ఇక్కడ లాగిన్ చేయండి", dashboard: "డాష్బోర్డ్", uploadPhoto: "ఫోటోను అప్లోడ్ చేయండి", uploadSubtitleShort: "మీ గ్యాలరీ నుండి ఎంచుకోండి", scanPhoto: "ఫోటోను స్కాన్ చేయండి", scanSubtitleShort: "మీ కెమెరాను నేరుగా ఉపయోగించండి", userProfile: "వినియోగదారు ప్రొఫైల్", profileSettings: "సెట్టింగులు", uploadTitle: "ఫోటోను అప్లోడ్ చేయండి", uploadSubtitle: "మీ గ్యాలరీ నుండి ఒక చిత్రాన్ని ఎంచుకోండి.", previewText: "చిత్ర పరిదృశ్యం ఇక్కడ కనిపిస్తుంది", selectImageBtn: "చిత్రాన్ని ఎంచుకోండి", submitScanBtn: "విశ్లేషణ కోసం సమర్పించండి", scanningTitle: "జంతువును స్కాన్ చేయండి", scanningSubtitle: "జంతువును ఫ్రేమ్‌లో ఉంచి క్యాప్చర్ చేయండి.", analyzingTitle: "విశ్లేషిస్తోంది...", analyzingSubtitle: "ఫీచర్లు సంగ్రహించబడుతున్నాయి మరియు స్కోరు లెక్కించబడుతోంది.", resultsTitle: "ఫలితాలు", resultsSubtitle: "ఇక్కడ మీ జంతువు యొక్క ATC స్కోర్ ఉంది.", annotatedImagePlaceholder: "వ్యాఖ్యానించబడిన చిత్రం ఇక్కడ ఉంటుంది", overallScoreLabel: "మొత్తం స్కోరు", menu: "మెను", securityAndPrivacy: "భద్రత & గోప్యత", helpAndSupport: "సహాయం & మద్దతు", signOut: "సైన్ అవుట్", editPersonalInfo: "వ్యక్తిగత సమాచారాన్ని సవరించండి", additionalFeatures: "అదనపు వినియోగదారు ఫీచర్లు", saveChanges: "మార్పులనుభద్రపరచు", currentPassword: "ప్రస్తుత పాస్వర్డ్", newPassword: "కొత్త పాస్వర్డ్", confirmNewPassword: "కొత్త పాస్వర్డ్ను నిర్ధారించండి", changePassword: "పాస్వర్డ్ను మార్చండి", faqs: "తరచుగా అడిగే ప్రశ్నలు", userGuide: "వినియోగదారు గైడ్", contactSupport: "మద్దతును సంప్రదించండి", privacyPolicy: "గోప్యతా విధానం", termsOfService: "సేవా నిబంధనలు", appVersion: "యాప్ వెర్షన్ 1.0.0", loginHeader: "లాగిన్ అవ్వండి", loginUsernameLabel: "వినియోగదారు పేరు", loginPasswordLabel: "పాస్వర్డ్", loginSubmitLabel: "లాగిన్ అవ్వండి", loginSwitchPrompt: "ఖాతా లేదా?", loginSwitchLink: "నమోదు చేసుకోండి", viewMoreDetails: "మరిన్ని వివరాలను చూడండి", traitScoresTitle: "లక్షణాల స్కోర్లు", traitBodyLength: "శరీర పొడవు:", traitWithersHeight: "మూపురం ఎత్తు:", traitHipHeight: "తుంటి ఎత్తు:", traitChestDepth: "ఛాతీ లోతు:", traitBodyWidth: "శరీర వెడల్పు:", retakeButton: "మళ్ళీ తీయి", submitButton: "సమర్పించు", faqTitle: "తరచుగా అడిగే ప్రశ్నలు", faqQ1: "బోవిలెన్స్ అంటే ఏమిటి?", faqA1: "బోవిలెన్స్ అనేది ఒక మొబైల్ యాప్, ఇది మీ ఫోన్ కెమెరా ద్వారా మీ పశువుల భౌతిక లక్షణాలను విశ్లేషించడానికి ఆర్టిఫిషియల్ ఇంటెలిజెన్స్ (AI)ను ఉపయోగిస్తుంది. ఇది జంతువు యొక్క శరీర నిర్మాణం మరియు నాణ్యతను త్వరగా అంచనా వేయడంలో మీకు సహాయపడటానికి తక్షణ \"ATC స్కోర్\" ఇస్తుంది.", faqQ2: "ఈ యాప్ ఎవరి కోసం?", faqA2: "ఈ యాప్ పాడి రైతులు, పశువుల పెంపకందారులు, పశువుల వ్యాపారులు మరియు పశువైద్య నిపుణుల కోసం రూపొందించబడింది, వీరు పశువులను అంచనా వేయడానికి శీఘ్ర మరియు ఆధునిక మార్గాన్ని కోరుకుంటారు.", faqQ3: "\"ATC స్కోర్\" అంటే ఏమిటి?", faqA3: "ATC (జంతు లక్షణాల నిర్ధారణ) స్కోర్ అనేది శరీర పొడవు, భుజాల ఎత్తు మరియు ఛాతీ లోతు వంటి ముఖ్య భౌతిక లక్షణాల ఆధారంగా 1 నుండి 5 వరకు రేటింగ్. అధిక స్కోర్ సాధారణంగా ప్రామాణిక ప్రజనన సూత్రాల ప్రకారం మెరుగైన భౌతిక నిర్మాణం మరియు రూపాన్ని సూచిస్తుంది.", faqQ4: "ఖచ్చితమైన స్కోర్ కోసం ఉత్తమ ఫోటోను ఎలా తీయాలి?", faqA4: "అత్యంత ఖచ్చితమైన ఫలితాల కోసం, జంతువు సమతలంగా ఉన్న నేపై నిలబడి ఉందని నిర్ధారించుకోండి. తల నుండి తోక వరకు పూర్తి శరీరాన్ని సంగ్రహిస్తూ, పక్క నుండి ఫోటో తీయండి. ముదురు నీడలను నివారించి, మంచి, స్పష్టమైన పగటి వెలుతురు ఉండేలా చూసుకోండి.", faqQ5: "స్కోర్ 100% ఖచ్చితమైనదా?", faqA5: "మా AI చాలా ఖచ్చితమైనదిగా ఉండటానికి వేలాది జంతువుల చిత్రాలపై శిక్షణ పొందింది. అయినప్పటికీ, స్కోర్‌ను మీ నిర్ణయానికి సహాయపడటానికి ఒక సూచన సాధనంగా ఉపయోగించాలి. దీన్ని ఎల్లప్పుడూ మీ స్వంత అనుభవంతో మరియు పశువైద్యుని సలహాతో పాటు ఉపయోగించడం ఉత్తమం.", faqQ6: "యాప్‌ను ఉపయోగించడానికి నాకు ఇంటర్నెట్ కనెక్షన్ అవసరమా?", faqA6: "అవును. మీరు ఫోటోను సమర్పించినప్పుడు మీకు సక్రియ ఇంటర్నెట్ కనెక్షన్ (Wi-Fi లేదా మొబైల్ డేటా) అవసరం. విశ్లేషణ అనేది మా సురక్షిత సర్వర్‌లలో జరిగే సంక్లిష్ట ప్రక్రియ.",
    }
};


let currentLanguage = 'en';
let cameraStream = null;
const blindsOverlay = document.getElementById('blinds-transition-overlay');

// --- THIS FUNCTION IS NOW FIXED TO PREVENT THE RACE CONDITION ---
async function checkAuthStatus() {
    const maxWaitTime = 3000; // Wait a maximum of 3 seconds
    const intervalTime = 100; // Check every 100ms
    let elapsedTime = 0;

    const intervalId = setInterval(async () => {
        // Check if the Capacitor libraries are loaded and ready
        if (window.Capacitor && window.Capacitor.Plugins) {
            clearInterval(intervalId); // Stop checking
            runAuthLogic(); // Run the real logic
            return;
        }
        
        elapsedTime += intervalTime;
        if (elapsedTime >= maxWaitTime) {
            // We've waited long enough. Assume Capacitor won't load (e.g., non-native browser)
            clearInterval(intervalId); // Stop checking
            console.log('Capacitor timed out or not available. Proceeding to login flow.');
            proceedToLoginFlow();
        }
    }, intervalTime);

    const runAuthLogic = async () => {
        const { Preferences } = window.Capacitor.Plugins;
        const { value } = await Preferences.get({ key: 'accessToken' });
        if (value) {
            console.log('User is already logged in.');
            fetchAnalysisHistory();
            showScreen('dashboard-screen');
        } else {
            console.log('User needs to log in.');
            proceedToLoginFlow();
        }
    };

    const proceedToLoginFlow = () => {
        setTimeout(() => { document.getElementById('splash-screen')?.classList.add('fade-out'); }, 250);
        setTimeout(() => { showScreen('language-screen'); }, 750);
    };
}


// --- API FUNCTIONS ---
async function registerUser(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    if (data.password !== data.confirm_password) {
        alert("Passwords do not match!");
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: data.username,
                full_name: data.full_name,
                password: data.password
            }),
        });

        const result = await response.json();
        if (!response.ok) {
            alert(`Registration failed: ${result.detail}`);
        } else {
            alert("Registration successful! Please log in.");
            showScreen('secure-login-screen');
            form.reset();
        }
    } catch (error) {
        console.error('Registration error:', error);
        alert("An error occurred. Please check the console and make sure the backend is running.");
    }
}

async function loginUser(event) {
    event.preventDefault();
    const { Preferences } = window.Capacitor.Plugins;
    const form = event.target;
    const formData = new FormData(form);
    const body = new URLSearchParams();
    body.append('username', formData.get('username'));
    body.append('password', formData.get('password'));

    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: body,
        });

        const result = await response.json();
        if (!response.ok) {
            alert(`Login failed: ${result.detail}`);
        } else {
            await Preferences.set({
                key: 'accessToken',
                value: result.access_token
            });
            fetchAnalysisHistory();
            showScreen('dashboard-screen');
            form.reset();
        }
    } catch (error) {
        console.error('Login error:', error);
        alert("An error occurred during login. Please ensure the backend is running.");
    }
}

async function analyzeImage(event) {
    event.preventDefault();
    const { Preferences } = window.Capacitor.Plugins;
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];
    const { value: token } = await Preferences.get({ key: 'accessToken' });

    if (!file) {
        alert("Please select an image first.");
        return;
    }
    if (!token) {
        alert("You must be logged in to perform an analysis.");
        showScreen('secure-login-screen');
        return;
    }

    showScreen('analyzing-screen');

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_BASE_URL}/analysis/`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` },
            body: formData,
        });

        const result = await response.json();

        if (!response.ok) {
            alert(`Analysis failed: ${result.detail}`);
        } else {
            populateResults(result);
            showScreen('results-screen');
        }
    } catch (error) {
        console.error('Analysis error:', error);
        alert("An error occurred during analysis. Please ensure the backend is running.");
    }
}

async function captureAndAnalyzeImage(event) {
    event.preventDefault();
    const { Preferences } = window.Capacitor.Plugins;
    const canvas = document.getElementById('photo-canvas');
    const { value: token } = await Preferences.get({ key: 'accessToken' });

    if (!canvas) return;
    if (!token) {
        alert("You must be logged in to perform an analysis.");
        showScreen('secure-login-screen');
        return;
    }

    showScreen('analyzing-screen');

    canvas.toBlob(async (blob) => {
        const formData = new FormData();
        formData.append('file', blob, 'capture.jpg');

        try {
            const response = await fetch(`${API_BASE_URL}/analysis/`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` },
                body: formData,
            });

            const result = await response.json();

            if (!response.ok) {
                alert(`Analysis failed: ${result.detail}`);
            } else {
                populateResults(result);
                showScreen('results-screen');
            }
        } catch (error) {
            console.error('Analysis error from capture:', error);
            alert("An error occurred during analysis. Please ensure the backend is running.");
        }
    }, 'image/jpeg');
}

async function fetchAndDisplayUserData() {
    const { Preferences } = window.Capacitor.Plugins;
    const { value: token } = await Preferences.get({ key: 'accessToken' });
    if (!token) {
        showScreen('secure-login-screen');
        return;
    }
    try {
        const response = await fetch(`${API_BASE_URL}/users/me`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) {
            throw new Error('Failed to fetch user data');
        }
        const userData = await response.json();
        populateProfileForm(userData);
    } catch (error) {
        console.error('Error fetching user data:', error);
    }
}

async function saveProfileChanges(event) {
    event.preventDefault();
    const { Preferences } = window.Capacitor.Plugins;
    const { value: token } = await Preferences.get({ key: 'accessToken' });
    if (!token) return;

    const nameInput = document.getElementById('edit-info-name');
    const updatedData = { full_name: nameInput.value };

    try {
        const response = await fetch(`${API_BASE_URL}/users/me`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatedData)
        });
        if (!response.ok) {
            const errorResult = await response.json();
            alert(`Failed to save changes: ${errorResult.detail}`);
        } else {
            alert("Profile updated successfully!");
        }
    } catch (error) {
        console.error('Error saving profile changes:', error);
    }
}

async function changePassword(event) {
    event.preventDefault();
    const { Preferences } = window.Capacitor.Plugins;
    const { value: token } = await Preferences.get({ key: 'accessToken' });
    if (!token) return;

    const form = document.getElementById('change-password-form');
    const currentPassword = form.elements['current_password'].value;
    const newPassword = form.elements['new_password'].value;
    const confirmNewPassword = form.elements['confirm_new_password'].value;

    if (newPassword !== confirmNewPassword) {
        alert("New passwords do not match.");
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/users/me/password`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                current_password: currentPassword,
                new_password: newPassword
            })
        });

        const result = await response.json();
        if (!response.ok) {
            alert(`Error: ${result.detail}`);
        } else {
            alert(result.message);
            form.reset();
            showScreen('dashboard-screen');
        }
    } catch (error) {
        console.error('Error changing password:', error);
    }
}

async function fetchAnalysisHistory() {
    const { Preferences } = window.Capacitor.Plugins;
    const { value: token } = await Preferences.get({ key: 'accessToken' });
    if (!token) return;

    try {
        const response = await fetch(`${API_BASE_URL}/analysis/history`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
            const history = await response.json();
            populateDashboardHistory(history);
        } else {
            console.error("Failed to fetch analysis history.");
        }
    } catch (error) {
        console.error("Error fetching history:", error);
    }
}

// --- RESTORED CORE FUNCTIONS ---
function setLanguage(lang) {
    currentLanguage = lang;
    document.querySelectorAll('[data-key]').forEach(element => {
        const key = element.getAttribute('data-key');
        if (translations[lang] && translations[lang][key]) {
            element.textContent = translations[lang][key];
        }
    });
    document.querySelectorAll('[data-key-placeholder]').forEach(element => {
        const key = element.getAttribute('data-key-placeholder');
        if (translations[lang] && translations[lang][key]) {
            element.placeholder = translations[lang][key];
        }
    });
}

function showScreen(screenId) {
    document.querySelectorAll('main, section').forEach(screen => {
        screen.classList.remove('visible');
        screen.classList.add('hidden');
    });
    const targetScreen = document.getElementById(screenId);
    if (targetScreen) {
        targetScreen.classList.remove('hidden');
        setTimeout(() => {
            targetScreen.classList.add('visible');
        }, 50);
    }
}

function setupBlinds() {
    if (!blindsOverlay) return;
    blindsOverlay.innerHTML = '';
    const blindCount = 50;
    for (let i = 0; i < blindCount; i++) {
        const blind = document.createElement('div');
        blind.className = 'blind';
        blind.style.left = `${i * 2}%`;
        blind.style.transition = `height ${400 + i * 15}ms ease-in-out`;
        blindsOverlay.appendChild(blind);
    }
}

function openSidebar() {
    document.getElementById('sidebar')?.classList.remove('-translate-x-full');
    document.getElementById('sidebar-backdrop')?.classList.remove('hidden');
}

function closeSidebar() {
    document.getElementById('sidebar')?.classList.add('-translate-x-full');
    document.getElementById('sidebar-backdrop')?.classList.add('hidden');
}

async function startCamera() {
    const videoElement = document.getElementById('camera-feed');
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia && videoElement) {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
            cameraStream = stream;
            videoElement.srcObject = stream;
        } catch (error) {
            console.error("Error accessing camera:", error);
        }
    }
}

function stopCamera() {
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
    }
}

function updateGauge(score) {
    const gaugeContainer = document.querySelector('.gauge-container');
    const gaugeValueElement = document.querySelector('.gauge-value');
    if (!gaugeContainer || !gaugeValueElement) return;
    const finalScore = Math.max(0, Math.min(5, score));
    gaugeValueElement.textContent = finalScore.toFixed(1);
    const percentage = (finalScore / 5);
    const degrees = percentage * 360;
    let color = '#1a4578';
    if (finalScore > 3.5) color = '#10b981';
    if (finalScore < 2.5) color = '#f59e0b';
    gaugeContainer.style.background = `conic-gradient(${color} ${degrees}deg, #e5e7eb ${degrees}deg)`;
}

function populateResults(result) {
    console.log('API Result:', result);
    if (result.overall_score) {
        updateGauge(result.overall_score);
    }
    const annotatedImage = document.getElementById('annotated-image');

    if (annotatedImage && result.annotated_image_url && result.annotated_image_url.trim() !== '') {
        annotatedImage.src = `${API_BASE_URL}${result.annotated_image_url}`;
        annotatedImage.alt = "Annotated analysis result";
    } else if (annotatedImage) {
        annotatedImage.src = "";
        annotatedImage.alt = "Analysis result not available";
    }

    const detailsContainer = document.getElementById('trait-details-list');
    if (detailsContainer && result.trait_scores) {
        detailsContainer.innerHTML = '';

        if (result.animal_type) {
            const animalLi = document.createElement('li');
            animalLi.className = 'trait-item';
            animalLi.innerHTML = `<span>Animal Type:</span><span class="font-bold">${result.animal_type.charAt(0).toUpperCase() + result.animal_type.slice(1)}</span>`;
            detailsContainer.appendChild(animalLi);
        }

        result.trait_scores.forEach(item => {
            const li = document.createElement('li');
            li.className = 'trait-item';
            li.innerHTML = `<span>${item.trait_name}:</span><span class="font-bold">${item.score}</span>`;
            detailsContainer.appendChild(li);
        });
    }
}

function populateProfileForm(user) {
    if (!user) return;
    const nameInput = document.getElementById('edit-info-name');
    if (nameInput) nameInput.value = user.full_name;
}

function populateDashboardHistory(history) {
    const historyContainer = document.getElementById('analysis-history-list');
    if (!historyContainer) return;

    historyContainer.innerHTML = '';

    if (history.length === 0) {
        historyContainer.innerHTML = '<p class="text-center text-gray-400">No analysis history yet.</p>';
        return;
    }

    history.forEach(item => {
        const date = new Date(item.timestamp).toLocaleDateString();
        const card = document.createElement('div');
        card.className = 'history-card bg-white p-4 rounded-lg shadow-md flex items-center space-x-4';
        
        card.innerHTML = `
            <img src="${API_BASE_URL}${item.annotated_image_url}" alt="Analysis thumbnail" class="w-16 h-16 rounded-md object-cover">
            <div class="flex-1">
                <p class="font-bold text-slate-800">Overall Score: ${item.overall_score}</p>
                <p class="text-sm text-slate-500">${date}</p>
            </div>
            <button type="button" class="view-history-details-btn p-2 rounded-full hover:bg-gray-200">
                <svg class="h-6 w-6 text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
            </button>
        `;
        historyContainer.appendChild(card);
    });
}
// --- EVENT LISTENERS ---
window.addEventListener('load', () => {
    setupBlinds();
    const dateElement = document.getElementById('dashboard-date');
    if (dateElement) {
        dateElement.textContent = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
    }
    checkAuthStatus();
});

document.querySelectorAll('.language-btn').forEach(button => {
    button.addEventListener('click', () => {
        const lang = button.getAttribute('data-lang');
        if (blindsOverlay) {
            blindsOverlay.style.display = 'block';
            setTimeout(() => { blindsOverlay.classList.add('animate'); }, 10);
            setTimeout(() => {
                setLanguage(lang);
                showScreen('secure-login-screen');
                blindsOverlay.style.display = 'none';
                blindsOverlay.classList.remove('animate');
            }, 1200);
        } else {
            setLanguage(lang);
            showScreen('secure-login-screen');
        }
    });
});

document.getElementById('login-form')?.addEventListener('submit', loginUser);
document.getElementById('register-form')?.addEventListener('submit', registerUser);

document.getElementById('show-register-link')?.addEventListener('click', (e) => {
    e.preventDefault();
    showScreen('register-screen');
});

document.getElementById('register-screen')?.querySelector('#show-login-link')?.addEventListener('click', (e) => {
    e.preventDefault();
    showScreen('secure-login-screen');
});

document.getElementById('file-input')?.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        const imagePreview = document.getElementById('image-preview');
        reader.onload = function(e) {
            imagePreview.innerHTML = ''; 
            const img = document.createElement('img');
            img.src = e.target.result;
            img.className = 'w-full h-full object-cover rounded-2xl';
            imagePreview.appendChild(img);
        }
        reader.readAsDataURL(file);
    }
});

document.getElementById('submit-upload-btn')?.addEventListener('click', analyzeImage);
document.getElementById('go-to-upload-btn')?.addEventListener('click', (e) => { e.preventDefault(); showScreen('upload-screen'); });
document.getElementById('go-to-camera-btn')?.addEventListener('click', (e) => { e.preventDefault(); showScreen('scanning-screen'); startCamera(); });

document.getElementById('capture-btn')?.addEventListener('click', (e) => {
    e.preventDefault();
    const video = document.getElementById('camera-feed');
    const canvas = document.getElementById('photo-canvas');
    const capturedImagePreview = document.getElementById('captured-image-preview');
    if (!video || !canvas || !capturedImagePreview) return;
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    capturedImagePreview.src = canvas.toDataURL('image/jpeg');
    capturedImagePreview.classList.remove('hidden');
    video.classList.add('hidden');
    document.getElementById('capture-btn').classList.add('hidden');
    document.getElementById('capture-controls').classList.remove('hidden');
    stopCamera();
});

document.getElementById('retake-btn')?.addEventListener('click', (e) => {
    e.preventDefault();
    document.getElementById('camera-feed').classList.remove('hidden');
    document.getElementById('capture-btn').classList.remove('hidden');
    document.getElementById('captured-image-preview').classList.add('hidden');
    document.getElementById('capture-controls').classList.add('hidden');
    startCamera();
});

document.getElementById('submit-capture-btn')?.addEventListener('click', captureAndAnalyzeImage);

// Back Buttons
document.getElementById('back-to-dashboard-btn')?.addEventListener('click', (e) => { e.preventDefault(); showScreen('dashboard-screen'); });
document.getElementById('back-to-dashboard-from-camera-btn')?.addEventListener('click', (e) => { e.preventDefault(); stopCamera(); showScreen('dashboard-screen'); });
document.getElementById('back-to-dashboard-from-results-btn')?.addEventListener('click', (e) => { e.preventDefault(); showScreen('dashboard-screen'); });
document.getElementById('back-to-dashboard-from-settings-btn')?.addEventListener('click', (e) => { e.preventDefault(); showScreen('dashboard-screen'); });

document.getElementById('view-details-btn')?.addEventListener('click', (e) => {
    const detailsContainer = document.getElementById('trait-details');
    if (detailsContainer) {
        detailsContainer.classList.toggle('hidden');
    }
});

document.getElementById('open-sidebar-btn')?.addEventListener('click', openSidebar);
document.getElementById('close-sidebar-btn')?.addEventListener('click', closeSidebar);
document.getElementById('sidebar-backdrop')?.addEventListener('click', closeSidebar);
document.getElementById('menu-dashboard-btn')?.addEventListener('click', (e) => { e.preventDefault(); closeSidebar(); showScreen('dashboard-screen'); });
document.getElementById('menu-profile-btn')?.addEventListener('click', (e) => {
    e.preventDefault();
    closeSidebar();
    fetchAndDisplayUserData();
    showScreen('edit-info-screen');
});
document.getElementById('menu-security-btn')?.addEventListener('click', (e) => { e.preventDefault(); closeSidebar(); showScreen('security-screen'); });
document.getElementById('menu-help-btn')?.addEventListener('click', (e) => { e.preventDefault(); closeSidebar(); showScreen('help-screen'); });
document.getElementById('menu-signout-btn')?.addEventListener('click', async (e) => {
    e.preventDefault();
    const { Preferences } = window.Capacitor.Plugins;
    await Preferences.remove({ key: 'accessToken' });
    closeSidebar();
    showScreen('secure-login-screen');
});

document.getElementById('go-to-edit-info-btn')?.addEventListener('click', (e) => {
    e.preventDefault();
    fetchAndDisplayUserData();
    showScreen('edit-info-screen');
});
document.getElementById('go-to-security-btn')?.addEventListener('click', (e) => { e.preventDefault(); showScreen('security-screen'); });
document.getElementById('go-to-help-btn')?.addEventListener('click', (e) => { e.preventDefault(); showScreen('help-screen'); });
document.getElementById('go-to-additional-btn')?.addEventListener('click', (e) => { e.preventDefault(); showScreen('additional-screen'); });
document.getElementById('go-to-faq-btn')?.addEventListener('click', (e) => { e.preventDefault(); showScreen('faq-screen'); });

document.querySelectorAll('.back-to-settings-btn').forEach(button => {
    button.addEventListener('click', (e) => {
        e.preventDefault();
        showScreen('settings-screen');
    });
});

document.querySelectorAll('.back-to-help-btn').forEach(button => {
    button.addEventListener('click', (e) => {
        e.preventDefault();
        showScreen('help-screen');
    });
});

document.getElementById('save-changes-form')?.addEventListener('submit', saveProfileChanges);
document.getElementById('change-password-form')?.addEventListener('submit', changePassword);

