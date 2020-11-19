<template>
    <div class="category">
<!--        分类按钮-->
        <div id="tab_bt">
            <el-button @click="s0">校园</el-button>
            <el-button @click="s1">焦点</el-button>
            <el-button @click="s2">财经</el-button>
            <el-button @click="s3">科技</el-button>
            <el-button @click="s4">文化</el-button>
            <el-button @click="s5">教育</el-button>
            <el-button @click="s6">深度</el-button>
            <el-button @click="s7">娱乐</el-button>
            <el-button @click="s8">时尚</el-button>
            <el-button @click="s9">体育</el-button>
        </div>
<!--        热点问题列表-->
        <div class="hotlist">
            <li id="li_id" v-for="(que, index) in ques" class="list-item" style="line-height: 30px">
                <el-card id="card">
                    <img id="image" src="../assets/logo.png">
                    <div id="content">
                        <h3><a href="javascript:void(0);" v-on:click="toQuestion(que)">{{que.title}}</a></h3>
                    </div>
                    <div style="margin: 60px 0;"></div>
                    <div class="some_count">
                        <el-button class='some_count_bt' icon="el-icon-view" @click="toQuestion(que)" circle></el-button>&nbsp;{{que.view_count}}
                        <el-button class='some_count_bt' icon="el-icon-star-off" @click="addCollect(que.id)" circle></el-button>&nbsp;{{que.collect_count}}
                        <el-button class='some_count_bt' icon="el-icon-chat-line-round" @click="toQuestion(que)" circle></el-button>&nbsp;{{que.answer_count}}
                    </div>
                </el-card>
            </li>
        </div>

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
                            <el-button class='some_count_bt' icon="el-icon-star-off" @click="addCollect(cur_que.id)" circle></el-button>&nbsp;{{cur_que.collect_count}}
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
                                <img class="avatar" src='../assets/logo.png'>
                                <el-button type="text" class="author" @click="aboutUser(ans.username)">{{ans.username}}</el-button>
                                <el-button type="info" id="report" icon="el-icon-warning" @click="tipoff(ans)" size="small" title="举报" circle></el-button>
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

<!--        用户信息对话框-->
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
<!--        举报表单对话框-->
        <el-dialog id="tip_dialog" :visible.sync="dialogTipVisible" width="800px">
            <el-card width="700px">
                <el-form ref="tipform" :model="tipForm" label-width="80px">
                    <el-form-item label="原因">
                        <el-input v-model="tipForm.reason"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="tipSubmit">提交</el-button>
                    </el-form-item>
                </el-form>
            </el-card>
        </el-dialog>
    </div>
</template>

<script>
    export default {
        name: "Home",
        data(){
            return {
                // 被点击的问题数据
                cur_que: {
                    id: '',
                    title: '',
                    description: '',
                    view_count: '',
                    collect_count: '',
                    gmt_create: '',
                    answers: [
                        // id, username, avatar_url, content, upvote, time
                    ]
                },
                dialogTableVisible: false,
                dialogUserVisible: false,
                dialogTipVisible: false,
                category: 'campus',
                // 展示问题数据
                ques: [
                    // id, title, description, view_count, answer_count, collect_count, gmt_create
                ],
                // 来自提交表单的数据
                answerArea: '',
                // about用户信息
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
                tipForm: {
                    reason: '',
                    username: '',
                    content: ''
                }
            }
        },
        created() {
            this.getData();
        },
        methods: {
            // 获取问题列表，按分类
            getData(){
                var vm = this;
                this.$http.get('getquestion', {params:{category: this.category, page: 0}})
                .then(function(response){
                    var data = response.data.data;
                    data.forEach((item, index)=>{
                        vm.ques.push(item);
                    })
                })
            },
            // 打开渲染详情页面
            toQuestion(que){
                var username = localStorage.getItem('token');
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
                // 加载id问题的回答
                this.$http.get('getanswer', {params:{idq: id}})
                .then(function (response) {
                    var data = response.data.data;
                    data.forEach((item, index)=>{
                        console.log(item);
                        vm.cur_que.answers.push(item);
                    })
                })
                this.dialogTableVisible = true;
                // 浏览记录questoin history
                this.$http.post('addhistory', 'username='+username+'&idq='+id);
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
                // 回答通知notification
                this.$http.get('newanswer', {params: {idq: id}});
            },
            addCollect(id){
                var username = localStorage.getItem('token');
                var idq = id;
                var vm = this;
                this.$http.post('addcollection', 'username='+username+'&idq='+idq)
                .then(function (response) {
                    if(response.data === 'success'){
                        vm.$message.success('收藏+1');
                    }else{
                        vm.$message.error('请勿重复收藏。');
                    }
                })
            },
            addUpvote(id){
                var username = localStorage.getItem('token');
                var ida = id;
                var vm = this;
                // 提交点赞
                this.$http.post('addupvote', 'username='+username+'&ida='+ida)
                .then(function (response) {
                    if(response.data === 'success'){
                        vm.$message.success('点赞+1');
                    }else{
                        vm.$message.error('请勿重复点赞。');
                    }
                })
                // 点赞通知notification
                this.$http.get('newupvote', {params: {username: username, ida: ida}})
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
            tipoff(ans){
                this.tipForm.username = ans.username;
                this.tipForm.content = ans.content;
                this.dialogTipVisible = true;
            },
            tipSubmit(){
                var vm = this;
                var username = this.tipForm.username;
                var content = this.tipForm.content;
                var reason = this.tipForm.reason;
                this.$http.post('tipoff', 'username='+username+'&content='+content+'&reason='+reason)
                .then(function (response) {
                    if(response.data === 'success'){
                        vm.$message.success('举报提交成功');
                    }else{
                        vm.$message.error('举报提交失败');
                    }
                });
            },
            resetInput(){
                this.answerArea = '';
            },
            // 按钮选择cate
            s0(){
                this.category = 'campus';
                this.ques = [];
                this.getData();
            },
            s1(){
                this.category = 'focus';
                this.ques = [];
                this.getData();
            },
            s2(){
                this.category = 'finance';
                this.ques = [];
                this.getData();
            },
            s3(){
                this.category = 'technology';
                this.ques = [];
                this.getData();
            },
            s4(){
                this.category = 'culture';
                this.ques = [];
                this.getData();
            },
            s5(){
                this.category = 'education';
                this.ques = [];
                this.getData();
            },
            s6(){
                this.category = 'depth';
                this.ques = [];
                this.getData();
            },
            s7(){
                this.category = 'entertain';
                this.ques = [];
                this.getData();
            },
            s8(){
                this.category = 'fashion';
                this.ques = [];
                this.getData();
            },
            s9(){
                this.category = 'sports';
                this.ques = [];
                this.getData();
            }
        }
    }
</script>

<style scoped>
    .category{
        margin: 0 auto;
        width: 790px;
        background-image: linear-gradient(-225deg, #CBBACC 0%, #2580B3 100%);
    }

    #tabs_bt{

    }

    #card{
        margin-left: 20px;
        margin-right: 20px;
    }

    #question_card{
        background-image: linear-gradient(-225deg, #CBBACC 0%, #2580B3 100%);
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

    #content{
        text-align: left;
        position: relative;
        left: 30px;
    }

    .some_count{
        float: right;
        padding-bottom: 10px;
    }

    .some_count_bt{
        border: 1px solid #7bbfea;
    }


    #li_id{
        list-style-type: none;
        margin-bottom: 50px;
    }

    #in_li_id{
        list-style-type: none;
        margin-bottom: 30px;
    }

    .hotlist{
        background-image: linear-gradient(-225deg, #CBBACC 0%, #2580B3 100%);
        margin-top: 20px;
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

    #dialog{

    }

    .time{
        font-size: 12px;
        float: right;
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

    #report{
        float: right;
    }
</style>