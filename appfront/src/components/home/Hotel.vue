<template>
    <div>
        <div style="margin-top: 400px;margin-bottom: 30px;text-align: left">
            <span style="font-size: 25px;font-weight: bold">为您推荐</span>
            <el-divider></el-divider>
        </div>
            <div style="height: 50px">
        <div style="height: 50px;float: left">
        <input
                placeholder="搜索酒店..."
                class="text"
                v-model="keywords"/>
        </div>
        <el-button  class="searchButton" @click="searchCommodities(keywords)"></el-button>
    </div>
        <div style="height: 1250px;width: 100%">
            <el-tooltip effect="dark" placement="right"
                        v-for="(item,index) in commodities.slice((currentPage-1)*pagesize,currentPage*pagesize)"
                        :key="item.id">
                <p slot="content" style="font-size: 14px;margin-bottom: 6px;">{{item.comname}}</p>
                <p slot="content" style="font-size: 13px;margin-bottom: 6px"><span>{{item.gift}}</span></p>
                <p slot="content" style="width: 300px" class="abstract">{{item.name}}</p>
                <el-card v-if = "index % 5 !== 4" class="card" bodyStyle="padding:10px" shadow="hover">
                    <div class="pic" v-on:click="getDetail(item)">
                        <img :src="item.piclink" alt="酒店图片">
                    </div>
                    <div class="info">
                        <div class="comname">
                            {{item.comname}}
                        </div>
                        <div class="sales">
                            人气：{{item.sales}}
                        </div>
                        <div class="favorrate">
                            好评率：{{item.favorrate * 100}}%
                        </div>
                        <div class="price">
                            {{item.newestprice}}
                        </div>
                    </div>
                </el-card>
                <el-card v-else class="card1" bodyStyle="padding:10px" shadow="hover">
                    <div class="pic" @click="getDetail(item)"> <!--修改click-->
                        <img :src="item.piclink" alt="商品图片">
                    </div>
                    <div class="info">
                        <div class="comname">
                            {{item.comname}}
                        </div>

                        <div class="sales">
                            人气：{{item.sales}}
                        </div>
                        <div class="favorrate">
                            好评率：{{item.favorrate * 100}}%
                        </div>
                        <div class="price">
                            {{item.newestprice}}
                        </div>
                    </div>
                </el-card>
            </el-tooltip>
        </div>
        <div style="height: 50px;width: 100px;margin: 50px auto auto;">
            <el-pagination
                    @current-change="handleCurrentChange"
                    :current-page="currentPage"
                    :page-size="pagesize"
                    :total="commodities.length">
            </el-pagination>
        </div>
    </div>
</template>

<script>
import SearchBar from '@/components/home/SearchBar.vue'

    export default {
        name: "Hotels",
        components: {SearchBar},
        data(){
            return {
                commodities:[],
                currentPage:1,
                pagesize:20,
                keywords: ''
            }
        },
        mounted:function() {
            this.loadCommodities()
        },
        methods: {
            searchCommodities(keywords) {
                console.log("searchItem");
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
            loadCommodities() {
                this.$axios.get('/hotels').then(resp => {
                    if (resp && resp.status === 200) {
                        this.commodities = resp.data.data;
                        console.log(this.commodities.length)
                    }
                })
            },
            handleCurrentChange: function (currentPage) {
                this.currentPage = currentPage
                //console.log(this.currentPage)
            },
            getDetail(item) {
                this.$store.commit('setInfo', item)
                this.$router.replace('/HotelInfo')
            }
        }
    }
</script>

<style scoped>
    .sales{
        width: 50%;
        float: left;
        text-align: left;
        font-size: 13px;
        color: #cac6c6;
    }
    .favorrate{
        width: 50%;
        float: right;
        text-align: left;
        font-size: 13px;
        color: #cac6c6;
    }
    .card {
        width: 19%;
        margin-bottom: 20px;
        height: 300px;
        float: left;
        margin-right: 1%;
    }
    .card1 {
        width: 19%;
        margin-bottom: 20px;
        height: 300px;
        float: right;
    }
    .pic {
        width: 100%;
        height: 100%;
        margin-bottom: 7px;
        overflow: hidden;
        cursor: pointer;
    }
    img {
        width: 100%;
        height: 200px;
        /*margin: 0 auto;*/
    }
    .comname {
        color: #333333;
        font-size: 16px;
        width: 100%;   /*一定要设置宽度，或者元素内含的百分比*/
        overflow:hidden; /*溢出的部分隐藏*/
        white-space: nowrap; /*文本不换行*/
        text-overflow:ellipsis;/*ellipsis:文本溢出显示省略号（...）；clip：不显示省略标记（...），而是简单的裁切*/
        margin-bottom: 8px;
    }
    .price{
        color:  #1baeae;
        font-size: 20px;
        width: 100%;
        margin-top: 35px;
        text-align: center;
    }
    .abstract {
        display: block;
        line-height: 17px;
    }
    a {
        text-decoration: none;
    }
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