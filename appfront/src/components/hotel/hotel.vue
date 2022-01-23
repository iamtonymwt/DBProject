<template>
  <div>
    <el-container style="width: 100%; margin: auto">
      <el-header>
        <div style="width: 100%">
          <div style="width: 100%">
            <Header></Header>
          </div>
          <div class="dc">
            <div class="title">
              <span style="margin-left: 10px; margin-bottom: 30px"
                >酒店详情</span
              >
            </div>
            <div class="fr">
              <li><a>用户评价</a></li>
              <li><a>|</a></li>
              <li><a>价格走势</a></li>
              <li><a>|</a></li>
              <li><a>概述</a></li>
            </div>
          </div>
        </div>
      </el-header>
      <el-main style="width: 70%; margin: auto">
        <div style="margin-top: 120px; width: 100%">
          <div style="float: left; width: 50%; height: 500px">
            <el-image
              style="width: 100%; height: 100%"
              :src="hotel.piclink"
            ></el-image>
          </div>
          <div class="infoField">
            <div class="comnameField">
              <span>{{ hotel.name }}</span>
            </div>
            <div class="addressField">
              <span>{{ hotel.address }}</span>
            </div>
            <div class="priceField">
              <div class="priceItem" :style="conHeight">
                <div class="discountItem">
                  <span class="discountLabel">价格</span>
                  <span class="discount">¥{{ hotel.newestprice }}(起)</span>
                </div>
              </div>
              <div style="width: 100%">
                <span class="scoreLabel">评分</span>
                <el-rate
                  v-model="hotel.favorrate"
                  disabled
                  show-score
                  text-color="#ff9900"
                >
                </el-rate>
              </div>
            </div>

            <div style="width: 100%">
              <el-button
                class="button"
                v-on:click="collect"
                icon="el-icon-star-off"
                type="detail"
                >收藏</el-button
              >
              <el-button
                class="button"
                v-on:click="goPage(hotel.url)"
                type="detail"
                >直达链接</el-button
              >
            </div>
          </div>
        </div>
      </el-main>
      <div style="width: 70%; margin: auto">
        <el-divider content-position="center">价格走势</el-divider>
        <Graph ref="graphArea"></Graph>
        <div v-show="this.hotel.platform === 'local'">
          <el-divider content-position="center">房间预订</el-divider>
          <div class="block">
            <el-date-picker
              v-model="duration"
              type="datetimerange"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              :default-time="['12:00:00']"
            >
            </el-date-picker>
            <el-button type="detail" style="font-size: 18px; font-weight: bold" @click="queryRoomInfo()"
              >查询</el-button
            >
            <el-card class="box-card" v-show="afterQuery">
              <div
                style="text-align: left"
                v-for="item in this.roomInfo"
                :key="item.id"
              >
                <div style="text-align: left; margin-left: 20px">
                  <el-card class="box-card">
                    <span>{{ item.type }}    </span>
                    <span>¥{{ item.price }}/天    </span>
                    <span>剩余{{ item.remain }}间    </span>
                    <el-button
                      type="detail"
                      style="font-size: 18px; font-weight: bold"
                      @click="book(item.id)"
                      >预订</el-button
                    >
                  </el-card>
                </div>
              </div>
            </el-card>
          </div>
        </div>
        <el-divider content-position="center">评分</el-divider>
        <div>
          <span>评价：</span>
          <el-rate v-model="score_value" show-text> </el-rate>
          <el-button
            v-on:click="addScore(score_value)"
            class="scoreButton"
            type="detail"
            icon="el-icon-edit"
            circle
            >打分</el-button
          >
        </div>

        <el-divider content-position="center">相关评论</el-divider>
        <Message
          class="message-area"
          ref="messageArea"
          style="width: 100%"
        ></Message>
      </div>
    </el-container>
    <div style="margin-top: 50px">
      <Footer></Footer>
    </div>
  </div>
</template>

<script>
import Header from "@/components/home/Header";
import Message from "@/components/hotel/Message";
import Graph from "@/components/hotel/Graph";
import Footer from "@/components/home/Footer";
export default {
  name: "CommodityInfo",
  components: { Footer, Graph, Message, Header },
  data() {
    return {
      score_value: null,
      conHeight: {
        height: "",
      },
      hotel: "",
      divNums: 4,
      platformMemberDiscountDetail: [],
      roomInfo: [
        { id: 1, type: "单人房", price: "120", remain: 2 },
        { id: 2, type: "双人房", price: "180", remain: 4 },
      ],
      duration: "",
      afterQuery: false,
    };
  },
  mounted: function () {
    this.hotel = this.$store.state.hotel;
    if (this.commodity === "") {
      this.$router.replace("/mainpage");
    }
  },
  async created() {
    this.getParams();
    if (this.hotel === "") {
      return;
    }
    //获取留言和回复
    this.getLeaveMessage();
    this.getPrice();
    this.addHistory();
  },
  methods: {
    addHistory() {
      if (this.hotel === "") {
        return;
      }
      this.$axios
        .post("/addHistory/", {
          hotel_id: this.hotel.cid,
          userid: this.$store.state.user.id,
          time: this.getMyTime(),
        })
        .then((resp) => {
          if (resp && resp.data.code === 200) {
            //
          } else {
            //
          }
        });
    },
    addScore(score) {
      if (this.hotel === "") {
        return;
      }
      this.$axios
        .post("/addScore/", {
          hotel_id: this.hotel.cid,
          userid: this.$store.state.user.id,
          score: score,
          time: this.getMyTime(),
        })
        .then((resp) => {
          if (resp && resp.data.code === 200) {
            this.$alert("打分成功", "提示", {
              confirmButtonText: "确定",
            });
          } else {
            this.$alert("网络问题，打分失败", "提示", {
              confirmButtonText: "确定",
            });
          }
        });
    },
    book(id) {
        this.$axios.post('/book/', {
          hotel_id: this.hotel.cid,
          userid: this.$store.state.user.id,
          time: this.getMyTime(),
        }).then((resp) => {
          if (resp && resp.data.code === 200) {
            this.$alert("预订成功", "提示", {
              confirmButtonText: "确定",
            });
          } else {
            this.$alert("预订失败", "提示", {
              confirmButtonText: "确定",
            });
          }
        });
    },
    queryRoomInfo() {
      this.$axios.post('/queryRoomInfo/', {duration: this.duration, hotel_id: this.hotel.cid}).then((resp) => {
          if (resp && resp.data.code === 200) {
            this.roomInfo = resp.data.roomInfo;
            this.afterQuery = true;
          } else {
            this.$alert("查询失败，请稍后重试", "提示", {
              confirmButtonText: "确定",
            });
          }
        });
    },
    collect() {
      if (this.hotel === "") {
        this.$alert("网络问题，收藏失败", "提示", {
          confirmButtonText: "确定",
        });
        return;
      }
      this.$axios
        .post("/addCollection/", {
          hotel: this.hotel.cid,
          userid: this.$store.state.user.id,
          time: this.getMyTime(),
        })
        .then((resp) => {
          if (resp && resp.data.code === 200) {
            this.$alert("收藏成功", "提示", {
              confirmButtonText: "确定",
            });
          } else {
            this.$alert("网络问题，收藏失败", "提示", {
              confirmButtonText: "确定",
            });
          }
        });
    },
    getPrice() {
      if (this.hotel === "") {
        return;
      }
      this.$axios.post("/price/", { hotel_id: this.hotel.cid }).then((resp) => {
        if (resp && resp.status === 200) {
          var i;
          for (i = 0; i < resp.data.data.length; i++) {
            this.$refs.graphArea.chartData.rows.push({
              日期: resp.data.data[i].date,
              价格: resp.data.data[i].price,
            });
          }
          //this.$refs.messageArea.leaveMessage = resp.data.data
        }
      });
    },
    getParams() {
      this.hotel = this.$store.state.hotel;
    },
    getLeaveMessage() {
      this.hotel = this.$store.state.hotel;
      this.$axios
        .post("/leavemessage/", { hotel_id: this.hotel.cid })
        .then((resp) => {
          if (resp && resp.status === 200) {
            this.$refs.messageArea.leaveMessage = resp.data.data;
            this.getReplyMessage();
          }
        });
    },
    async getReplyMessage() {
      var i;
      var _this = this;
      for (i = 0; i < _this.$refs.messageArea.leaveMessage.length; i++) {
        var id = _this.$refs.messageArea.leaveMessage[i].id;
        await this.$axios
          .post("/replymessage/", { message: "aa", leaveMessage_id: id })
          .then((resp) => {
            if (resp && resp.status === 200) {
              //this.$refs.messageArea.replyMessage.push({id:resp.data.data})
              //console.log(id)
              this.$refs.messageArea.replyMessage[id] = resp.data.data;
            }
          });
      }
    },
    goPage(url) {
      //window.location.href = url
      window.open(url, "_blank");
    },
  },
};
</script>

<style scoped>
.fr {
  width: 50%;
  float: right;
  list-style-type: none;
  margin-top: 8px;
}
.title {
  width: 300px;
  height: 38px;
  line-height: 58px;
  font-size: 22px;
  font-weight: bold;
  float: left;
  text-align: left;
  margin-top: -8px;
}
.dc {
  width: 70%;
  margin: auto;
  margin-top: 100px;
  height: 38px;
  background: #f0f0f0;
}
.ml20 {
  margin-left: 20px;
}
.tb-extra {
  font-size: 13px;
  margin-top: 20px;
  height: 100px;
  width: 55%;
  float: left;
}
.button {
  float: right;
  margin-right: 50px;
  background-color: #1baeae;
  color: white;
  width: 120px;
}
.icons {
  text-align: left;
  font-size: 14px;
  color: #cac6c6;
  height: 100px;
  float: bottom;
  background-color: #333333;
}
.cont {
  text-decoration: none;
  color: #b0b0b0;
}
li {
  width: auto;
  margin: 0 0 0 0;
  margin-left: 10px;
  float: right;
}
dl {
  width: 100%;
  text-align: center;
  float: left;
  margin: 5px;
}
.storeField {
  font-size: 16px;
  text-align: left;
  margin-top: 20px;
  width: 100%;
}
.giftField {
  font-size: 16px;
  text-align: left;
  margin-top: 20px;
  color: #b0b0b0;
  width: 100%;
}
.comnameField {
  font-size: 32px;
  font-weight: bold;
  text-align: center;
  width: 100%;
}
.infoField {
  float: left;
  width: 50%;
  height: 500px;
  background-color: #f8f8f8;
}
.addressField {
  font-size: 16px;
  text-align: center;
  width: 100%;
}
.priceField {
  margin-top: 20px;
  color: #1baeae;
  font-weight: bolder;
  font-size: 20px;
  float: right;
  width: 100%;
  height: 100px;
}
.priceItem {
  float: right;
  width: 100%;
  text-align: right;
}
.discountItem {
  margin: auto auto auto auto;
  width: 100%;
  float: right;
}
.discountLabel {
  color: #cac6c6;
  font-weight: normal;
  font-size: 16px;
  margin-right: 40px;
  float: left;
}
.scoreLabel {
  color: #cac6c6;
  font-weight: normal;
  font-size: 12px;
  margin-right: 40px;
  float: left;
}
.discount {
  color: #1baeae;
  font-weight: normal;
  font-size: 32px;
}
.el-button--detail:focus,
.el-button--detail:hover {
  background: #48d1cc;
  border-color: #48d1cc;
  color: #fff;
}
.el-button--detail {
  color: #fff;
  background-color: #20b2aa;
  border-color: #20b2aa;
}
.storeButton {
  float: right;
  background-color: #1baeae;
  color: white;
}
</style>

