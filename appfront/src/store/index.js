import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)

export default new Vuex.Store({
    namespaced: true,
    state:{
        user:{
            id: window.localStorage.getItem('id') === null ? '' :JSON.parse(window.localStorage.getItem('id')),
            username: window.localStorage.getItem('username') === null ? '' :JSON.parse(window.localStorage.getItem('username')),
            email:window.localStorage.getItem('email') === null ? '' :JSON.parse(window.localStorage.getItem('email')),
            date:window.localStorage.getItem('date') === null ? '' :JSON.parse(window.localStorage.getItem('date')),
            type:window.localStorage.getItem('type') == null ? '' :JSON.parse(window.localStorage.getItem('type')),
            loc_hotel:window.localStorage.getItem('loc_hotel') == null ? '' :JSON.parse(window.localStorage.getItem('loc_hotel'))
        },
        adminMenus: [],
        hotel:'',
    },
    mutations: {
        login(state, userInfo) {
            state.user.id = userInfo.id
            state.user.username = userInfo.username
            state.user.email = userInfo.email
            state.user.date = userInfo.date
            state.user.type = userInfo.type
            state.user.loc_hotel = userInfo.loc_hotel
            window.localStorage.setItem('id', JSON.stringify(userInfo.id))
            window.localStorage.setItem('username', JSON.stringify(userInfo.username))
            window.localStorage.setItem('email', JSON.stringify(userInfo.email))
            window.localStorage.setItem('date', JSON.stringify(userInfo.date))
            window.localStorage.setItem('loc_hotel', JSON.stringify(userInfo.loc_hotel))
        },
        logout(state) {
            state.user = {
                id:'',
                username:'',
                email:'',
                loc_hotel:'',
            }
            window.localStorage.removeItem('id')
            window.localStorage.removeItem('username')
            window.localStorage.removeItem('email')
            window.localStorage.removeItem('type')
            window.localStorage.removeItem('loc_hotel')
        },
        initAdminMenu (state, menus) {
            state.adminMenus = menus
        },
        setInfo(state, hotel) {
            state.hotel = hotel
            window.localStorage.setItem('hotel', JSON.stringify(hotel))
        },
        getInfo(state) {
            console.log(state.hotel.id)
            return window.localStorage.getItem('hotel')
        }
    }
})