export function getUserId(): string {
    let userId = localStorage.getItem("userId");
    if (!userId) {
        userId = crypto.randomUUID(); // Genera un ID único
        localStorage.setItem("userId", userId);
    }
    return userId;
}

export const resetUserSession = () => {
    localStorage.removeItem("userId");
};