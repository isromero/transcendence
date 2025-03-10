export const API_URL = 'http://localhost:8000/api';
export const PORT = 3001;
// export const CLIENT_ID = 'u-s4t2ud-37ff4a4c74679b10b03bab47f05a4d1bc70f63b012fa95a7fefeed85f4996c80';
// export const CLIENT_SECRET = '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';
export const CLIENT_ID = process.env.OAUTH42_CLIENT_ID;
export const CLIENT_SECRET = process.env.OAUTH42_CLIENT_SECRET;
export const REDIRECT_URI = 'http://localhost:8000/auth/callback/';

// OAUTH42_CLIENT_ID=u-s4t2ud-37ff4a4c74679b10b03bab47f05a4d1bc70f63b012fa95a7fefeed85f4996c80
// OAUTH42_CLIENT_SECRET=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
// OAUTH42_REDIRECT_URI=http://localhost:8000/auth/callback/