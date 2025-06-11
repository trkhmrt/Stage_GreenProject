import axios from "axios";




export const authLogin = async (data) => {
        const response = await axios.post("http://localhost:8099/auth/login", data);
        console.log(response)
        localStorage.setItem("activeBasketId",response.data.activeBasketId);
        localStorage.setItem("customerId",response.data.customerId);
        console.log("Giriş başarılı, token:", response.data.accessToken);
        return response;
};


export const authLogout = () =>{}