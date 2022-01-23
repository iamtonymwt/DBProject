<template>
    <div class="footer">
        <div class="top">
            <div style="width: 100px;height: 150px;float: left">
            </div>
            <div style="height: 50px;float: left;width: 100px">
                <div style="height: 30px;width: 100%">
                    <span style="color: #eaeaea;line-height: 50px;float: left;margin-left: 10px">人工客服</span>
                </div>
                <div style="height:50px;width: 100%">
                    <span style="color: #eaeaea;float: left;margin-left: 10px">110-120-119</span>
                </div >
                <div style="height: 50px;width: 100%">
                    <el-button size="mini" style="background: #333333;color: #eaeaea;
                                font-size: 12px;">在线咨询</el-button>
                </div>
            </div>
            <div style="height: 50px;float: left;width: 100px;margin-left: 100px">
                <div style="height: 30px;width: 100%">
                    <span style="color: #eaeaea;line-height: 50px;float: left;margin-left: 10px">账户管理</span>
                </div>
                <div style="height:50px;width: 100%">
                    <span style="color: #eaeaea;float: left;margin-left: 10px">购物指南</span>
                </div >
                <div style="height: 50px;width: 100%">
                    <span style="color: #eaeaea;float: left;margin-left: 10px;margin-top: 5px">关于我们</span>
                </div>
            </div>
            <div style="height: 50px;float: left;width: 100px;margin-left: 100px">
                <div style="height: 30px;width: 100%">
                    <span style="color: #eaeaea;line-height: 50px;float: left;margin-left: 10px"><a href="https://www.elong.com/">艺龙网</a></span>
                </div>
                <div style="height:50px;width: 100%">
                    <span style="color: #eaeaea;float: left;margin-left: 10px"><a href="https://hotels.ctrip.com/">携程网</a></span>
                </div >
                <div style="height: 50px;width: 100%">
                    <span style="color: #eaeaea;float: left;margin-left: 10px;margin-top: 5px"><a href="https://www.qunar.com/">去哪儿网</a></span>
                </div>
            </div>
            <div style="height: 50px;float: left;width: 100px;margin-left: 100px">
                <div style="height: 30px;width: 100%">
                    <span style="color: #eaeaea;line-height: 50px;float: left;margin-left: 10px"><a href="">了解我们</a></span>
                </div>
                <div style="height:50px;width: 100%">
                    <span style="color: #eaeaea;float: left;margin-left: 10px">加入我们</span>
                </div >
                <div style="height: 50px;width: 100%">
                    <span style="color: #eaeaea;float: left;margin-left: 10px;margin-top: 5px">捐赠维护</span>
                </div>
            </div>
            <div style="height: 150px;float: right;width: 150px">
                <div >
                    <!-- <img style="height: 100px;width: 100px;margin-top: 10px" src="../../assets/myQR.jpg"> -->
                </div>
            </div>
        </div>
        <div class="middle">
            <div>
                <span style="font-size:10px;color: #eaeaea;float: left;margin-left: 10px;margin-top: 5px">友情链接：</span>
            </div>
            <div>
                <span style="font-size:10px;color: #eaeaea;float: left;margin-left: 10px;margin-top: 5px"><a href="https://github.com/SunzeY/DBProject">GitHub地址</a></span>
            </div>
        </div>
        <div class="bottom">
            <div>
                <span style="font-size:10px;color: #42b983;margin: auto">数据库大作业项目</span>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Footer"
    }
</script>

<style scoped>
    .top{
        height: 60%;
        width: 70%;
        margin: auto;
    }
    .middle{
        height: 20%;
        width: 70%;
        margin: auto;
    }
    .bottom{
        height: 20%;
        width: 70%;
        margin: auto;
    }
    .footer {
        height: 200px;
        background: #333333;
        width: 100%;
    }
    a{
        text-decoration:none ;
        color:white ;
    }
</style>