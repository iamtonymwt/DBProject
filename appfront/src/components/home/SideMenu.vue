<template>
<el-dialog
                :show-close="false"
                title="排行榜"
                :visible.sync="dialogFormVisible">
<el-tabs type="border-card"
class="categories"
            default-active="0"
            @select="handleSelect"
            active-text-color="#1baeae">
  <el-tab-pane label="低价榜" style="width=60%">
    <el-table :data="tableDataByPrice" :row-class-name="tableRowClassName"> 
    <el-table-column prop="hotelName" label="酒店名">
    </el-table-column>
    <el-table-column prop="price" label="单人间价格"> </el-table-column>
  </el-table>
  </el-tab-pane>
  <el-tab-pane label="好评榜">
      <el-table :data="tableDataByCom" :row-class-name="tableRowClassName"> 
    <el-table-column prop="hotelName" label="酒店名">
    </el-table-column>
    <el-table-column prop="score" label="评分"> </el-table-column>
  </el-table>
  </el-tab-pane>
  <el-tab-pane label="人气榜">
      <el-table :data="tableDataByPop" :row-class-name="tableRowClassName"> 
      <el-table-column prop="hotelName" label="酒店名">
    </el-table-column>
    <el-table-column prop="popValue" label="人气值"> </el-table-column>
    </el-table> 
  </el-tab-pane>
</el-tabs>
</el-dialog>
</template>

<script>
export default {
  name: "SideMenu",
  data() {
    return {
      dialogFormVisible: false,
      tableDataByPrice: [],
      tableDataByCom: [],
      tableDataByPop: [],
    }
  },
  mounted:function() {
        this.loadRank()
  },
  methods: {
    tableRowClassName({ row, rowIndex }) {
      if (rowIndex === 0) {
        return "gold";
      } else if (rowIndex === 1) {
        return "silver";
      } else if (rowIndex === 2) {
        return "copper"  
      }
      return "";
    },
    loadRank() {
        this.$axios.get('/rankAll').then(
                    resp=>{
                        if (resp && resp.data.status === 200) {
                            this.tableDataByPrice = resp.data.data.tableDataByPrice;
                            this.tableDataByCom = resp.data.data.tableDataByCom;
                            this.tableDataByPop = resp.data.data.tableDataByPop;
                        }
                    }
                )
    }
  },
};
</script>

<style>
/* .categories{
        position: fixed;
        margin-left: 50%;
        left: -740px;
        top: 250px;
        width: 400px;
    } */
.el-table .gold {
  background: #ffeb93;
}

.el-table .silver {
  background: #e4e6e4;
}

.el-table .copper {
  background: #fcd4a0;
}

</style>