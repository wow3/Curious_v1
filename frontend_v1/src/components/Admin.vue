<template>

    <el-container>
        <el-header>
            <div id="title">
                <img id="logo" src="../assets/logo.png" alt="">
            </div>
            <div id="title_text">
                <h4>Admin</h4>
            </div>
            <div>
                <el-button id="exit_bt" type="info" round @click="logout">退出</el-button>
            </div>
        </el-header>
        <el-main>
            <el-card id="c">
                <el-tabs v-model="activeName" @tab-click="handleClick">
<!--                    用户管理-->
                    <el-tab-pane label="用户管理" name="first">
                        <el-table :data="tableData" stripe style="width: 100%">
                            <el-table-column prop="username" label="邮箱" width="240"></el-table-column>
                            <el-table-column prop="nickname" label="昵称" width="150"></el-table-column>
                            <el-table-column prop="gmt_create" label="用户创建时间" width="340"></el-table-column>
                            <el-table-column prop="banned" label="状态"></el-table-column>
                            <el-table-column fixed="right" label="操作" width="300">
                                <template slot-scope="scope">
                                    <el-button type="primary" @click="aboutUser(scope.row.username)">查看</el-button>
                                    <el-button type="danger" @click="banUser(scope.row.username)">封禁</el-button>
                                    <el-button type="info" @click="unbanUser(scope.row.username)">解禁</el-button>
                                </template>
                            </el-table-column>
                            <el-button>封禁</el-button>
                        </el-table>
                    </el-tab-pane>
<!--                    举报管理-->
                    <el-tab-pane label="举报管理" name="second">
                        <div id="noti_list">
                            <li id="li_id" v-for="(noti, index) in notis" class="list-item" style="line-height: 30px">
                                <el-card id="tipcard">
                                    <i class="time">{{noti.gmt_create}}+8</i>
                                    <el-divider></el-divider>
                                    <div id="tipcontent">
                                        {{noti.content}}
                                    </div>
                                    <el-divider></el-divider>
                                    <el-button id="mark_bt" type="primary" @click="isRead(noti.id)">已处理</el-button>
                                </el-card>
                            </li>
                        </div>
                    </el-tab-pane>

                </el-tabs>
            </el-card>
        </el-main>

        <el-dialog id="about_user" :visible.sync="dialogUserVisible" width="900px">
            <el-card width="835px">
                <el-card id="user">
                    <div id="dd">
                        <img id="avatar" :src="userinfo.avatar_url">
                        <div id="nime"><h4>{{userinfo.nickname}}</h4></div>
                    </div>
                    <el-card id="cc" shadow="hover">
                        <div id="demail">邮箱：{{userinfo.username}}</div>
                        <div id="dage">C 龄：{{userinfo.age}}天</div>
                    </el-card>
                </el-card>
                <el-card id="datadisp">
                    <ve-radar id="chart" :data="chartData" width="410px" height="400px"></ve-radar>
                </el-card>
                <el-card id="medal">
                    <h3>用户的成就</h3>
                    <div id="medals">
                        <img :src="medal_a" class="mymedal" title="回答数量">
                        <img :src="medal_v" class="mymedal" title="获赞数量">
                        <img :src="medal_r" class="mymedal" title="回答获赞比">
                    </div>
                </el-card>
            </el-card>
        </el-dialog>
    </el-container>

</template>
<script>
    export default {
        data() {
            return {
                activeName: 'first',
                tableData: [

                ],
                dialogUserVisible: false,
                userinfo: {
                    username: '',
                    nickname: '',
                    avatar_url: '',
                    age: ''
                },
                // about用户数据
                chartData: {
                    columns: ['对比', '回答数量', '获赞数量', '回答获赞比'],
                    rows: [

                    ]
                },
                medal_a: '',
                medal_v: '',
                medal_r: '',
                notis: [

                ]
            };
        },
        created() {
            this.getData();
        },
        methods: {
            handleClick(tab, event) {
                console.log(tab, event);
            },
            flush(){
                this.tableData = [];
                this.notis = [];
                this.getData();
            },
            getData(){
                var vm = this;
                this.$http.get('getuserlist')
                .then(function (response) {
                    var data = response.data.data;
                    data.forEach((item, index)=>{
                        vm.tableData.push(item);
                    })
                });
                this.$http.get('gettipoff')
                .then(function (response) {
                    var data = response.data.data;
                    data.forEach((item, index)=>{
                        vm.notis.push(item);
                    })
                });
            },
            aboutUser(username){
                var vm = this;
                this.userinfo.username = username
                this.$http.get('getuserinfo', {params: {username: vm.userinfo.username}})
                    .then(function (response) {
                        var data = response.data.data;
                        vm.userinfo.age = data.age;
                        vm.userinfo.nickname = data.nickname;
                        vm.userinfo.avatar_url = require('../assets/avatar/'+data.avatar_url);
                    })
                this.$http.get('countmyanswer', {params:{username: username}})
                    .then(function (response) {
                        var data = response.data.data;
                        var c_answer = data.c_answer;
                        var c_upvote = data.c_upvote;
                        var ratio = data.ratio;
                        var mydata = {'对比': '用户', '回答数量': c_answer, '获赞数量': c_upvote, '回答获赞比': ratio};
                        var avg_answer = data.avg_answer;
                        var avg_upvote = data.avg_upvote;
                        var avg_ratio = data.avg_ratio;
                        var avgdata = {'对比': '平均', '回答数量': avg_answer, '获赞数量': avg_upvote, '回答获赞比': avg_ratio};
                        vm.chartData.rows = [];
                        vm.chartData.rows.push(mydata);
                        vm.chartData.rows.push(avgdata);
                        if(c_answer > avg_answer){
                            vm.medal_a = require("../assets/medal/A1.png");
                        }else{
                            vm.medal_a = require("../assets/medal/A0.png");
                        }
                        if(c_upvote > avg_upvote){
                            vm.medal_v = require("../assets/medal/V1.png");
                        }else{
                            vm.medal_v = require("../assets/medal/V0.png");
                        }
                        if(ratio > avg_ratio){
                            vm.medal_r = require("../assets/medal/R1.png");
                        }else{
                            vm.medal_r = require("../assets/medal/R0.png");
                        }
                    });
                this.dialogUserVisible = true;
            },
            isRead(id){
                var vm = this;
                this.$http.get('markasread', {params:{id: id}})
                    .then(function (response) {
                        if(response.data === 'mark-success'){
                            vm.$message.success('标记成功');
                        }else{
                            vm.$message.error('标记失败');
                        }
                    });
                this.flush();
                this.$router.go(0);
            },
            banUser(username){
                var vm = this;
                this.$http.post('banuser', 'username='+username)
                .then(function (response) {
                    if(response.data === 'success'){
                        vm.$message.success('封禁成功');
                    }else{
                        vm.$message.error('封禁失败');
                    }
                });
                this.flush();
                this.$router.go(0);
            },
            unbanUser(username){
                var vm = this;
                this.$http.post('unban', 'username='+username)
                    .then(function (response) {
                        if(response.data === 'success'){
                            vm.$message.success('解禁成功');
                        }else{
                            vm.$message.error('解禁失败');
                        }
                    });
                this.flush();
                this.$router.go(0);
            },
            // 注销
            logout(){
                localStorage.clear()
                this.$router.push('/login')
            }
        }
    };
</script>

<style lang="less" scoped>
    #c{
        width: 1200px;
        margin: 0 auto;
    }

    .el-header{
        height: 120px;
    }

    .el-main{
        background-color: #2b4b6b;
    }

    #title{
        float: left;
    }

    #logo{
        height: 60px;
    }

    #title_text{
        float: right;
        position: relative;
        right: 200px;
    }

    #user{
        margin-bottom: 10px;
        height: 200px;
        background-image: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    #avatar{
        width: 100px;
        height: 100px;
        border-radius: 50%;
    }

    #nime{
        position: relative;
        left: 30px;
    }

    #datadisp{
        width: 450px;
        height: 400px;
        float: right;
    }

    #medal{
        float: left;
        height: 400px;
        width: 340px;
    }

    #dd{
        float: left;
    }

    #cc{
        height: 100px;
        width: 300px;
        float: left;
        background-color: white;
        position: center;
        position: relative;
        left: 50px;
    }

    #demail{

    }

    .el-button:hover{
        box-shadow: 2px 2px 2px #888888;
    }

    #dage{
        position: relative;
        top: 10px;
    }

    .mymedal{
        width: 120px;
        height: 120px;
        float: left;
    }

    #medals{
        padding-left: 50px;
    }

    #tipcard{
        width: 700px;
        margin: 0 auto;
    }

    .time{
        float: right;
    }

    #li_id{
        list-style-type: none;
        margin-bottom: 50px;
    }

    #mark_bt{
        float: right;
        margin-bottom: 10px;
    }

    #exit_bt{
        float: right;
        position: relative;
        top: 10px;
    }

</style>