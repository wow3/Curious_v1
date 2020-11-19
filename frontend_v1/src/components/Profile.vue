<template>
    <div>
        <el-card id="c">
            <el-tabs tab-position="left">
<!--                我的主页-->
                <el-tab-pane label="我的主页">
                    <el-card id="user">
                        <div id="dd">
                            <img id="avatar" :src="userinfo.avatar_url">
                            <div id="nime"><h4>{{nickname}}</h4></div>
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
                        <h3>我的成就</h3>
                        <div id="medals">
                            <img :src="medal_a" class="mymedal" title="回答数量">
                            <img :src="medal_v" class="mymedal" title="获赞数量">
                            <img :src="medal_r" class="mymedal" title="回答获赞比">
                        </div>
                    </el-card>
                </el-tab-pane>
<!--                我的收藏-->
                <el-tab-pane label="我的收藏">
                    <el-card id="collect_card">
                        <div id="collect_list">
                            <li id="col_li" v-for="(col, index) in collist">
                                <el-card id="in_card0">
                                    <div class="card_head">
                                        <i style="font-weight: bold; background-color: #7bbfea">{{col.category}}</i>
                                    </div>
                                    <el-divider></el-divider>
                                    <div id="colcont">
                                        <h3><a href="javascript:void(0);" v-on:click="toQuestion(col)">{{col.title}}</a></h3>
                                    </div>
                                    <div style="margin: 30px 0;"></div>
                                    <el-divider></el-divider>
                                    <div class="card_foot">
                                        <el-button class="some_count_bt" icon="el-icon-view"></el-button>&nbsp;{{col.view_count}}
                                        <el-button class="some_count_bt" icon="el-icon-star-off"></el-button>&nbsp;{{col.collect_count}}
                                        <el-button class="some_count_bt" icon="el-icon-chat-line-round"></el-button>&nbsp;{{col.answer_count}}
                                        <el-button id="del_bt" type="primary" icon="el-icon-delete"></el-button>
                                    </div>
                                </el-card>
                            </li>
                        </div>
                    </el-card>
                </el-tab-pane>
<!--                我的回答-->
                <el-tab-pane label="我的回答">
                    <el-card id="answer_card">
                        <div id="answer_list">
                            <li id="ans_li" v-for="(ans, index) in anslist">
                                <el-card id="in_card1">
                                    <div class="card_head">
                                        <i style="font-weight: bold">{{ans.title}}</i>
                                    </div>
                                    <el-divider></el-divider>
                                    <div id="anscont">
                                        <p>{{ans.content}}</p>
                                    </div>
                                    <div style="margin: 30px 0;"></div>
                                    <el-divider></el-divider>
                                    <div class="card_foot">
                                        <el-button class="some_count_bt" icon="el-icon-s-opportunity"></el-button>&nbsp;{{ans.upvote}}
                                        <i id="gmt">{{ans.gmt_create}}</i>
                                    </div>
                                </el-card>
                            </li>
                        </div>
                    </el-card>
                </el-tab-pane>
            </el-tabs>
        </el-card>

<!--        收藏点击进入详情页面-->
        <el-dialog id="dialog" :visible.sync="dialogTableVisible" width="700px">
            <el-card id="question_card">
                <h3>问题详情</h3>
                <!--            问题卡片-->
                <el-card id="que_card">
                    <i class="time">{{cur_col.gmt_create}}</i>
                    <el-divider></el-divider>
                    <div id="que_detail">
                        <h3 id="title">{{cur_col.title}}</h3>
                        <div style="margin: 20px 0;"></div>
                        <p id="descript">{{cur_col.description}}</p>
                        <div style="margin: 20px 0;"></div>
                        <div class="some_count">
                            <el-button class='some_count_bt' icon="el-icon-view" circle></el-button>&nbsp;{{cur_col.view_count}}
                            <el-button class='some_count_bt' icon="el-icon-star-off" circle></el-button>&nbsp;{{cur_col.collect_count}}
                        </div>
                    </div>
                </el-card>
            </el-card>
            <div style="margin: 50px 0;"></div>

            <el-card id="answer_card">
                <div id="answer_list" >
                    <h3>回答列表</h3>
                    <li id="in_li_id" v-for="(ans, index) in cur_col.answers" style="line-height: 30px">
                        <el-card id="in_card">
                            <div class="card_head">
                                <i class="author" style="position: relative; right: 240px">{{ans.username}}</i>
                                <i class="time">{{ans.gmt_create}}+8</i>
                            </div>
                            <el-divider></el-divider>
                            <div id="in_content">
                                <p>{{ans.content}}</p>
                            </div>
                            <div class="some_count">
                                <el-button class='some_count_bt' icon="el-icon-s-opportunity" @click="addUpvote(ans.id)" circle></el-button>&nbsp;{{ans.upvote}}
                            </div>
                        </el-card>
                    </li>
                </div>
            </el-card>

        </el-dialog>
    </div>
</template>

<script>
    export default {
        name: "Profile",
        data() {
            return {
                // 主页用户信息
                userinfo: {
                    username: '',
                    avatar_url: '',
                    age: ''
                },
                nickname: "",
                // 主页用户数据
                chartData: {
                    columns: ['对比', '回答数量', '获赞数量', '回答获赞比'],
                    rows: [

                    ]
                },
                // 我的收藏
                collist: [
                    // idq, title, category, description, view_count, collect_count, answer_count, gmt_create
                ],
                // 我的回答
                anslist: [
                    // id, content, upvote, gmt_create
                ],
                cur_col: {
                    id: '',
                    title: '',
                    description: '',
                    view_count: '',
                    collect_count: '',
                    gmt_create: '',
                    answers: [
                        // id, username, content, upvote, time
                    ]
                },
                dialogTableVisible: false,
                medal_a: '',
                medal_v: '',
                medal_r: ''
            }
        },
        created() {
            this.getData();
            this.getUserInfo();
            this.nickname = localStorage.getItem('nickname');
            this.getCollection();
            this.getAnswer();
        },
        methods: {
            getData(){
                var vm = this;
                var username = localStorage.getItem('token');
                this.$http.get('countmyanswer', {params:{username: username}})
                .then(function (response) {
                    var data = response.data.data;
                    var c_answer = data.c_answer;
                    var c_upvote = data.c_upvote;
                    var ratio = data.ratio;
                    var mydata = {'对比': '我', '回答数量': c_answer, '获赞数量': c_upvote, '回答获赞比': ratio};
                    var avg_answer = data.avg_answer;
                    var avg_upvote = data.avg_upvote;
                    var avg_ratio = data.avg_ratio;
                    var avgdata = {'对比': '平均', '回答数量': avg_answer, '获赞数量': avg_upvote, '回答获赞比': avg_ratio};
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
            },
            // 获取我的收藏
            getCollection(){
                var vm = this;
                var username = localStorage.getItem('token');
                this.$http.get('getmycollection', {params:{username, username}})
                .then(function (response) {
                    var data = response.data.data;
                    data.forEach((item, index)=>{
                        vm.collist.push(item);
                    })
                })
            },
            // 获取我的回答
            getAnswer(){
                var vm = this;
                var username = localStorage.getItem('token');
                this.$http.get('getmyanswer', {params:{username, username}})
                .then(function (response) {
                    var data = response.data.data;
                    data.forEach((item, index)=>{
                        vm.anslist.push(item);
                    })
                })
            },
            // 收藏问题的详情页面
            toQuestion(col){
                var username = localStorage.getItem('token');
                this.cur_col.id = col.idq;
                this.cur_col.title = col.title;
                this.cur_col.description = col.description;
                this.cur_col.view_count = col.view_count;
                this.cur_col.collect_count = col.collect_count;
                this.cur_col.gmt_create = col.gmt_create;
                this.cur_col.answers = []
                var vm = this;
                var id = col.idq;
                this.$http.get('getanswer', {params:{idq:id}})
                .then(function (response) {
                    var data = response.data.data;
                    data.forEach((item, index)=>{
                        vm.cur_col.answers.push(item);
                    })
                })
                this.dialogTableVisible = true;
            },
            getUserInfo(){
                this.userinfo.username = localStorage.getItem('token');
                var vm = this;
                this.$http.get('getuserinfo', {params: {username: vm.userinfo.username}})
                .then(function (response) {
                    var data = response.data.data;
                    vm.userinfo.age = data.age;
                    vm.userinfo.avatar_url = require('../assets/avatar/'+data.avatar_url);
                })
            }
        }
    }
</script>

<style scoped>
    #c{
        margin: 0 auto;
        width: 950px;
        background-image: linear-gradient(to right, #CBBACC 0%, #2580B3 100%);
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

    #col_li{
        list-style-type: none;
        margin-bottom: 50px;
    }

    #ans_li{
        list-style-type: none;
        margin-bottom: 50px;
    }

    .card_head{
        float:right;
    }

    #gmt{
        float:right;
    }

    #del_bt{
        float: right;
    }

    a:link {
        text-decoration: none;
        color: black;
    }

    a:hover {
        background-image: linear-gradient(to left, #ffecd2 0%, #fcb69f 100%);
    }

    .time{
        font-size: 12px;
        float: right;
    }

    #li_id{
        list-style-type: none;
        margin-bottom: 50px;
    }

    #in_li_id{
        list-style-type: none;
        margin-bottom: 30px;
    }

    #question_card{
        background-image: linear-gradient(-225deg, #CBBACC 0%, #2580B3 100%);
    }

    #answer_card{
        background-image: linear-gradient(-225deg, #CBBACC 0%, #2580B3 100%);
    }

    #collect_card{
        background-image: linear-gradient(-225deg, #CBBACC 0%, #2580B3 100%);
    }

    .mymedal{
        width: 120px;
        height: 120px;
        float: left;
    }

    #medals{
        padding-left: 50px;
    }
</style>