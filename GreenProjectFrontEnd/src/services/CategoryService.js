import axios from 'axios';


export const getAllCategories = async () => {
    return await axios.get("http://localhost:8088/category/getAllCategories");
}
