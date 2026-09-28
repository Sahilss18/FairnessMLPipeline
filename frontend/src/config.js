const isLocal = typeof window !== 'undefined' && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1');

const API_BASE_URL = process.env.REACT_APP_API_URL || (isLocal ? 'http://localhost:5000' : 'https://fairnessmlpipeline.onrender.com');

export { API_BASE_URL };

