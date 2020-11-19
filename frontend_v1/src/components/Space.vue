<template>
    <div>
<!--        推荐问题列表-->
        <el-card id="c">
            <div id="c_header">
                <h3>Here are some questions you may be interested in.</h3>
            </div>
            <div id="queslist">
                <li id="li_id" v-for="(que, index) in ques" class="list-item" style="line-height: 30px">
                    <el-card id="cc">
                        <i style="font-weight: bold; background-color: #7bbfea; float: right">{{que.category}}</i>
                        <el-divider></el-divider>
                        <div id="quecontent">
                            <h3><a href="javascript:void(0);" v-on:click="toQuestion(que)">{{que.title}}</a></h3>
                        </div>
                        <div style="margin: 60px 0;"></div>
                        <el-divider></el-divider>
                        <div class="some_count">
                            <el-button class='some_count_bt' icon="el-icon-view" circle></el-button>&nbsp;{{que.view_count}}
                            <el-button class='some_count_bt' icon="el-icon-star-off" circle></el-button>&nbsp;{{que.collect_count}}
                            <el-button class='some_count_bt' icon="el-icon-chat-line-round" circle></el-button>&nbsp;{{que.answer_count}}
                        </div>
                    </el-card>
                </li>
            </div>
        </el-card>

<!--        详情对话框-->
        <el-dialog id="dialog" :visible.sync="dialogTableVisible" width="700px">
            <el-card id="question_card">
                <h3>问题详情</h3>
                <!--            问题卡片-->
                <el-card id="que_card">
                    <i class="time">{{cur_que.gmt_create}}+8</i>
                    <el-divider></el-divider>
                    <div id="que_detail">
                        <h3 id="title">{{cur_que.title}}</h3>
                        <div style="margin: 20px 0;"></div>
                        <p id="descript">{{cur_que.description}}</p>
                        <div style="margin: 20px 0;"></div>
                        <div class="some_count">
                            <el-button class='some_count_bt' icon="el-icon-view" circle></el-button>&nbsp;{{cur_que.view_count}}
                            <el-button class='some_count_bt' icon="el-icon-star-off" circle></el-button>&nbsp;{{cur_que.collect_count}}
                        </div>
                    </div>
                </el-card>
            </el-card>
            <div style="margin: 50px 0;"></div>
<!--            回答列表-->
            <el-card id="answer_card">
                <div id="answer_list" >
                    <h3>回答列表</h3>
                    <li id="in_li_id" v-for="(ans, index) in cur_que.answers" style="line-height: 30px">
                        <el-card id="in_card">
                            <div class="card_head">
                                <img class="avatar" src="../assets/logo.png">
                                <el-button type="text" class="author" @click="aboutUser(ans.username)">{{ans.username}}</el-button>
                                <i class="time">{{ans.gmt_create}}+8</i>
                            </div>
                            <el-divider></el-divider>
                            <div id="in_content">
                                <p>{{ans.content}}</p>
                            </div>
                            <div class="some_count">
                                <i class="el-icon-s-opportunity">{{ans.upvote}}</i>&nbsp;&nbsp;&nbsp;
                            </div>
                        </el-card>
                    </li>
                </div>
            </el-card>
            <div style="margin: 50px 0;"></div>
<!--            编辑回答卡片-->
            <el-card id="edit_answer">
                <!--                回答键入区域-->
                <el-input type="textarea" :autosize="{ minRows: 5, maxRows: 100}" placeholder="请输入内容" v-model="answerArea"></el-input>
                <div style="margin: 20px 0;"></div>
                <div id="dbts">
                    <el-button class="dbt" type="primary" @click="addAnswer(cur_que.id)">提 交</el-button>
                    <el-button class="dbt" type="primary" @click="resetInput">重 置</el-button>
                </div>
            </el-card>
        </el-dialog>

        <el-dialog id="about_user" :visible.sync="dialogUserVisible" width="900px">
            <el-card width="835px">
                <el-card id="user">
                    <div id="dd">
                        <img id="avatar" :src="userinfo.avatar_url">
                        <div id="nime"><h4>{{userinfo.nickname}}</h4></div>
                    </div>
                    <el-card id="ccc" shadow="hover">
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
    </div>
</template>

<script>
    export default {
        name: "Space",
        data(){
            return {
                // 被点击的问题数据
                cur_que: {
                    id: '',
                    title: '',
                    description: '',
                    view_count: '',
                    collect_count: '',
                    answer_count: '',
                    gmt_create: '',
                    answers: [
                        // id, username, content, upvote, time
                    ]
                },
                dialogTableVisible: false,
                // 展示问题数据
                ques: [
                    // id, title, category, description, view_count, answer_count, collect_count, gmt_create
                ],
                // 来自提交表单的数据
                answerArea: '',
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
                medal_r: ''
            }
        },
        created() {
            this.getData();
        },

        methods: {
            // 获取计算好的推荐问题
            getData(){
                var vm = this;
                var username = localStorage.getItem('token');
                this.$http.get('getrecommend', {params:{username: username}})
                    .then(function(response){
                        var data = response.data.data;
                        data.forEach((item, index)=>{
                            vm.ques.push(item);
                        })
                    })
            },
            // 加载渲染问题详情页
            toQuestion(que){
                this.cur_que.id = que.id;
                this.cur_que.title = que.title;
                this.cur_que.description = que.description;
                this.cur_que.view_count = que.view_count;
                this.cur_que.collect_count = que.collect_count;
                this.cur_que.gmt_create = que.gmt_create;
                var id = que.id;
                // this.$message.success('加载'+id+'号问题！');
                var vm = this;
                this.cur_que.answers = [];
                this.$http.get('getanswer', {params:{idq: id}})
                    .then(function (response) {
                        var data = response.data.data;
                        data.forEach((item, index)=>{
                            console.log(item);
                            vm.cur_que.answers.push(item);
                        })
                    })
                this.dialogTableVisible = true;
            },
            // 提交回答  username, idq, content
            addAnswer(id){
                // this.$message.success('为'+id+'号问题提交答案');
                var username = localStorage.getItem('token');
                // this.$message.info(username);
                if(this.answerArea === ''){
                    this.$message.error('回答不能为空！');
                }else{
                    // this.$message.success('要提交了！');
                    var vm = this;
                    var content = this.answerArea;
                    this.$http.post('addanswer', 'username='+username+'&idq='+id+'&content='+content)
                        .then(function (response) {
                            if(response.data === 'add-success'){
                                vm.$message.success('提交成功！');
                            }else{
                                vm.$message.error('提交失败!');
                            }
                        })
                }
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
            resetInput(){
                this.answerArea = '';
            }
        }
    }
</script>

<style lang="less" scoped>
    .el-main{
        background-image: linear-gradient(to right, #E3FDF5 0%, #FFE6FA 100%);
    }

    #c{
        margin: 0 auto;
        width: 790px;
        background-image: linear-gradient(to right, #CBBACC 0%, #2580B3 100%);
    }

    #cc{
        margin-left: 20px;
        margin-right: 20px;
    }

    #question_card{
        background-image: linear-gradient(to right, #CBBACC 0%, #2580B3 100%);
    }

    #answer_card{
        background-image: linear-gradient(-225deg, #CBBACC 0%, #2580B3 100%);
    }

    #edit_answer{
        background-image: linear-gradient(-225deg, #CBBACC 0%, #2580B3 100%);
    }

    #image{
        width: 100px;
        float: left;
    }

    .el-button:hover{
        box-shadow: 2px 2px 2px #888888;
    }

    #quecontent{
        text-align: left;
        position: relative;
        left: 30px;
        padding-right: 10px;
    }

    .some_count{
        float: right;
        padding-bottom: 10px;
    }

    #li_id{
        list-style-type: none;
        margin-bottom: 50px;
    }

    #in_li_id{
        list-style-type: none;
        margin-bottom: 30px;
    }

    a:link {
        text-decoration: none;
        color: black;
    }

    a:hover {
        background-image: linear-gradient(to left, #ffecd2 0%, #fcb69f 100%);
    }

    .dbt{
        padding-right: 20px;
        background-color: #2b4b6b;
        border-width: 0;
        border-radius: 3px;
    }

    .dbt:hover{
        box-shadow: 2px 2px 2px #888888;
    }

    .time{
        font-size: 12px;
        float: right;
    }

    #c_header{
        padding-bottom: 50px;
        height: 50px;
        text-align: left;
    }

    .avatar{
        height: 10px;
        border-radius: 5px;
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

    #ccc{
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

</style>