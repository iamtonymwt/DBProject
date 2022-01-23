<template>
  <div>
    <div style="width: 100%; margin: auto">
      <el-container style="width: 100%; margin: auto">
        <el-header>
          <Header
            @onSearch="onSearch"
            ref="headerArea"
            style="width: 100%"
          ></Header>
          <el-button class="first" v-on:click="rank_visable" type="text" icon="el-icon-share">排行榜</el-button>
          <div style="width: 70%; margin-top: 100px; margin: auto">
            <recommend class="recommend-area"></recommend>
          </div>
        </el-header>
        <SideMenu
            @categorySelect="listByCategory"
            ref="sideMenuArea"
            style=""
          ></SideMenu>
        <el-main style="width: 80%; margin: auto">
          <Hotels
            class="commodities-area"
            ref="commoditiesArea"
          ></Hotels>
        </el-main>
      </el-container>
    </div>
    <div>
      <Footer></Footer>
    </div>
  </div>
</template>

<script>
import Header from "@/components/home/Header";
import Recommend from "@/components/home/Recommend";
import SideMenu from "@/components/home/SideMenu";
import Hotels from "@/components/home/Hotel";
import Footer from "@/components/home/Footer";
import SearchBar from "@/components/home/SearchBar";
export default {
  name: "Mainpage",
  components: {Footer, Header, Hotels, Recommend, SideMenu, SearchBar},
  methods: {
    rank_visable() {
      console.log("click rank");
      this.$refs.sideMenuArea.dialogFormVisible = true;
    },
    onSearch() {
      // this.$refs.commoditiesArea.searchCommodities(this.$refs.headerArea.keywords)
    },
    listByCategory() {
      // var cid = this.$refs.sideMenuArea.cid
      // if (cid === '0') {
      //     this.$refs.commoditiesArea.loadCommodities()
      //     return
      // }
      // var url = 'category/'+ cid
      // this.$axios.get(url).then(resp=>{
      //     if (resp && resp.status === 200) {
      //         this.$refs.commoditiesArea.commodities = resp.data.data
      //     }
      //     else {
      //         console.log("加载失败")
      //     }
      // })
    },
  },
};
</script>

<style scoped>

.first {
  left: -200px;
  top: 400px;
}
.recommend-area {
  margin-top: 100px;
  width: 100%;
}
.commodities-area {
  width: 100%;
  margin-top: 300px;
  margin-left: auto;
  margin-right: auto;
}
</style>