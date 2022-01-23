<template>
  <div>
    <div>
      <el-drawer
        title="选择视图"
        :visible.sync="drawer"
        :direction="direction"
        :before-close="handleClose"
      >
        <div>
          <el-select
            style="width: 100%"
            v-model="valueMember"
            placeholder="选择城市"
          >
            <el-option
              v-for="item in optionMember"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </div>
        <box class="typeChoose">
          <el-radio-group v-model="typeChoose">
            <el-radio-button label="价格"></el-radio-button>
            <el-radio-button label="好评度"></el-radio-button>
            <el-radio-button label="便捷度"></el-radio-button>
          </el-radio-group>
        </box>
        <box style="position: relative; top: +140px; left: +90px">
          <span style="position: relative; left: -290px">时间粒度</span>
          <div class="container">
            <div class="block">
              <span class="demonstration">周</span>
              <el-date-picker
                v-model="value1"
                type="week"
                format="yyyy 第 WW 周"
                placeholder="选择周"
              >
              </el-date-picker>
            </div>
            <div class="block">
              <span class="demonstration">月</span>
              <el-date-picker
                v-model="value2"
                type="month"
                placeholder="选择月"
              >
              </el-date-picker>
            </div>
          </div>
          <div class="container">
            <div class="block">
              <span class="demonstration">年</span>
              <el-date-picker v-model="value3" type="year" placeholder="选择年">
              </el-date-picker>
            </div>
          </div>
        </box>
        <el-button type="danger" style="position: relative; top:400px; left:80px" @click="value2='';value1='';value3=''">重置选项</el-button>
        <el-button type="primary" style="position: relative; top:400px; left:220px" @click="update()">更新</el-button>
      </el-drawer>
    </div>
    <div style="width: 100%; margin: auto">
      <el-container style="width: 100%; margin: auto">
        <el-header>
          <Header
            @onSearch="onSearch"
            ref="headerArea"
            style="width: 100%"
          ></Header>
        </el-header>
        <el-main style="width: 100%; margin: auto">
          <div style="width: 100%">
            <iframe
              src="https://maplab.amap.com/share/mapv/54ca6de6386c74661d9cb42315245fd6"
              width="1440"
              height="680"
            ></iframe>
          </div>
          <div class="settings">
            <el-button
              type="primary"
              icon="el-icon-edit"
              size="25px"
              circle
              @click="drawer = true"
            ></el-button>
          </div>
        </el-main>
      </el-container>
    </div>
  </div>
</template>

<script>
import Header from "@/components/home/Header";
import { map } from "../api/api.js";
export default {
  name: "map",
  components: { Header },
  data() {
    return {
      drawer: false,
      direction: "ltr",
      typeChoose: "价格",
      optionMember: [
        {
          value: "1",
          label: "北京市",
        },
      ],
      valueMember: [],
      value1: "",
      value2: "",
      value3: "",
    };
  },
  methods: {
    update() {
      this.$axios.post('/MapUpdate/', 
      {
        type: this.typeChoose, 
        year: this.value3,
        month: this.value2,
        day: this.value1
      }).then((resp) => {
          if (resp.data.code === 200) {
            this.$alert("更新成功", "提示", {
              confirmButtonText: "确定",
            });
            drawer = false;
          } else {
            this.$alert("更新失败，请重试", "提示", {
              confirmButtonText: "确定",
            });
          }
        });
    }
  },
};
</script>

<style scoped>
#settings {
  z-index: 2;
}
#map {
  position: fixed;
  width: 100%;
  height: 100;
  z-index: 3;
}
.settings {
  position: relative;
  top: -685px;
  height: 40px;
  width: 40px;
  border-radius: 20px;
  text-align: center;
  background-color: yellow;
}

.typeChoose {
  position: relative;
  top: +60px;
  left: +110px;
}
</style>