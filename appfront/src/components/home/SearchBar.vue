<template>
    <div style="height: 50px">
        <div style="height: 50px;float: left">
        <input
                placeholder="搜索酒店..."
                class="text"
                v-model="keywords"/>
        </div>
        <el-button  class="searchButton" @click="searchCommodities(keywords)"></el-button>
    </div>
</template>

<script>
    export default {
        name: "SearchBar",
        data () {
            return {
                keywords: '',
                commodities: [],
                cardLoading: []
            }
        },
        methods: {
            searchCommodities(keywords) {
                this.$axios
                    .post('/searchHotel/', {keyword: keywords}).then(resp => {
                    if (resp && resp.status === 200) {
                        this.commodities = resp.data.data
                        console.log(this.commodities)
                    }
                    else {
                        console.log("搜索失败")
                    }
                })
            },
            searchClick () {
                this.$emit('onSearch')
                this.$
            }
        }
    }
</script>

<style scoped>
    .text {
        box-sizing: border-box;
        width: 250px;
        height: 50px;
        border: 1px solid #ccc;
        padding: 0 10px;
    }
    .searchButton{
        box-sizing: border-box;
        height: 50px;
        width: 50px;
        text-indent: -10000px;;
        background: url(../../assets/search.png) no-repeat;
        background-size: 100%;
        background-position: center;
        background-color: #fff;
        border: 1px solid #ccc;
        cursor: pointer;
    }
</style>