import axios from "axios";

const serviceUrl = "http://localhost:8040/basket"


export const getBasketCustomerById = async(customerId) => {
    const response = await axios.get(`${serviceUrl}/basketProductListing/${customerId}`,{
        withCredentials: true,
    });
    localStorage.setItem("customerBasketId",response.data.basketId);
    console.log(response.data);
    return response.data;
}
export const getBasketBasketById = async(basketId) => {
    const response = await axios.get(`${serviceUrl}/getBasketProductUnitByBasketId/${basketId}`,);
    console.log(response.data);
    return response.data;
}


export const deleteProductFromBasket = async(productId) => {
    const basketId = localStorage.getItem("customerBasketId");
    const response = await axios.get(`${serviceUrl}/removeProductFromBasket/${basketId}/${productId}`);
    console.log(response.data);
    return response.data;
}

export const addProductToBasket = async(productId) => {
    const customerId = localStorage.getItem("customerId");
    const response = await axios.get(`${serviceUrl}/addProductToCustomerBasket/${customerId}/${productId}`);
    console.log(response.data);
    return response.data;
}


export const readyForCheckout = async (basketId) => {
    const response = await axios.put(`${serviceUrl}/ready-for-checkout/${basketId}`)
    return response.data;
}

export const decrementProductFromBasket = async(basketProductUnitId) => {
    return await axios.put(`${serviceUrl}/decrementProductQuantity/${basketProductUnitId}`);
}

export const incrementProductFromBasket = async(basketProductUnitId) => {
    return await axios.put(`${serviceUrl}/incrementProductQuantity/${basketProductUnitId}`);
}
