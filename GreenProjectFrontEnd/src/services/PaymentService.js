import axios from 'axios';

const serviceUrl = "http://localhost:8086/payment"

export const createPayment = async (paymentRequest) => {
    return axios.post(`${serviceUrl}/createPayment`, paymentRequest);
}