// appfront/src/api/api.js
import axiosInstance from './index'

const axios = axiosInstance

export const getUsers = () => {return axios.get(`http://localhost:8000/user/`)}
export const postUser = (email, password, username, type) => {return axios.post(`http://localhost:8000/user/`, {'username': username, 'email': email, 'password': password, 'type': type})}
export const login = (params, headers) => axios.post("http://localhost:8000/Login/", params, headers)
export const map = (params, headers) => axios.post("http://localhost:8000/map/", params, headers)

export const getHotels = () => {return axios.get('/Hotels')}