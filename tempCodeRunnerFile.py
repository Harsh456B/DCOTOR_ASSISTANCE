}
"""

with gr.Blocks(
    css=custom_css,
    title="🏥 Advanced AI Doctor - Multilingual Medical Assistant",
    theme=gr.themes.Soft(
        primary_hue="purple",
        secondary_hue="blue",
        neutral_hue="slate"
    )
) as demo:
    --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    --medical-blue: #2c5aa0;
    --medical-green: #00c9a7;
    --medical-red: #ff6b6b;
    --shadow-lg: 0 10px 40px rgba(0,0,0,0.15);
    --shadow-xl: 0 20px 60px rgba(0,0,0,0.25);
}

* {
    font-family: 'Poppins', 'Inter', sans-serif;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Responsive Container */
.gradio-container {
    max-width: 100% !important;
    width: 100% !important;
    padding: 10px !important;
    margin: 0 auto !important;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

@media (min-width: 768px) {
    .gradio-container {
        padding: 20px !important;
        max-width: 1400px !important;
    }
}

@media (min-width: 1200px) {
    .gradio-container {
        max-width: 1600px !important;
    }
}

/* Medical Header with Pulse Animation */
.medical-header {
    background: var(--primary-gradient);
    padding: 25px 15px !important;
    border-radius: 15px;
    text-align: center;
    color: white;
    margin-bottom: 25px;
    box-shadow: var(--shadow-lg);
    animation: slideDown 0.6s ease, pulse 2s infinite;
    position: relative;
    overflow: hidden;
}

.medical-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    animation: rotate 20s linear infinite;
}

@media (min-width: 768px) {
    .medical-header {
        padding: 40px !important;
        border-radius: 20px;
    }
}

@keyframes slideDown {
    from { transform: translateY(-50px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.01); }
}

@keyframes rotate {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.medical-header h1 {
    font-size: 28px !important;
    font-weight: 800 !important;
    margin: 0 !important;
    text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
    position: relative;
    z-index: 1;
}

@media (min-width: 768px) {
    .medical-header h1 {
        font-size: 42px !important;
    }
}

@media (min-width: 1200px) {
    .medical-header h1 {
        font-size: 52px !important;
    }
}

.medical-header p {
    font-size: 14px !important;
    margin-top: 10px !important;
    opacity: 0.95;
    position: relative;
    z-index: 1;
}

@media (min-width: 768px) {
    .medical-header p {
        font-size: 18px !important;
        margin-top: 15px !important;
    }
}

/* Feature Boxes with Hover Effects */
.feature-box {
    background: white;
    padding: 15px !important;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin: 12px 0 !important;
    border-left: 4px solid #667eea;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

@media (min-width: 768px) {
    .feature-box {
        padding: 20px !important;
        border-radius: 15px;
        margin: 15px 0 !important;
    }
}

.feature-box::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(102,126,234,0.1), transparent);
    transition: left 0.5s;
}

.feature-box:hover::before {
    left: 100%;
}

.feature-box:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: var(--shadow-lg);
    border-left-width: 6px;
}

/* Disclaimer Box with Animation */
.disclaimer-box {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
    color: white;
    padding: 18px !important;
    border-radius: 12px;
    margin: 15px 0 !important;
    box-shadow: 0 5px 20px rgba(255,107,107,0.4);
    text-align: center;
    font-weight: 600;
    animation: shake 5s infinite;
}

@media (min-width: 768px) {
    .disclaimer-box {
        padding: 25px !important;
        border-radius: 15px;
        margin: 20px 0 !important;
    }
}

@keyframes shake {
    0%, 98%, 100% { transform: translateX(0); }
    99% { transform: translateX(2px); }
}

/* Tabs Styling */
.tab-nav button {
    font-size: 14px !important;
    font-weight: 600 !impor