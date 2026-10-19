export {};

declare global {
  interface Window {
    __TELOCE_ROUTER__?: any; // Replace 'any' with your router's actual type if available
  }
}
