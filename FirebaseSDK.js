// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDar4RogfH1TQo1tDyItTQt6_LWbHtBOD4",
  authDomain: "pbl5-arduino.firebaseapp.com",
  databaseURL: "https://pbl5-arduino-default-rtdb.firebaseio.com",
  projectId: "pbl5-arduino",
  storageBucket: "pbl5-arduino.appspot.com",
  messagingSenderId: "370500106218",
  appId: "1:370500106218:web:cc072bddfe3d38fd312493",
  measurementId: "G-D310VN8Q6V"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);