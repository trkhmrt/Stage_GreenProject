import axios from "axios";


export const getAllProducts = async () => {
    const response = await axios.get(`http://localhost:8088/product/getAllProducts`);
    return response.data;
}

export const addProduct = async (product) => {
    return await axios.post(`http://localhost:8088/product/createProduct`,product);
}