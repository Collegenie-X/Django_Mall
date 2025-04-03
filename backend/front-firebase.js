// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBTFf3UNf9lgJ7oDLzNVZaBgpYv8Ee9_4w",
  authDomain: "jp-mall-71d90.firebaseapp.com",
  projectId: "jp-mall-71d90",
  storageBucket: "jp-mall-71d90.firebasestorage.app",
  messagingSenderId: "751234259835",
  appId: "1:751234259835:web:b51f20fd052e2b4c267bde",
  measurementId: "G-FBZGBRDT2G"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

export {auth}; 