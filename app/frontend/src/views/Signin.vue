<template>
  <v-app id="inspire">
    <v-main>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <v-alert
              class="mb-3"
              v-if="isLoginError"
              type="error" 
            >
              아이디 혹은 비밀번호가 틀립니다!
            </v-alert>
            <v-card class="elevation-12" max-width=400>
              <v-toolbar color="primary" dark>
                <v-toolbar-title class="text --white">로그인</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <validation-observer
                  ref="observer"
                >
                  <v-form>
                    <validation-provider
                      v-slot="{ errors }"
                      name="Name"
                      rules="required"
                    >
                      <v-text-field
                        prepend-icon="person"
                        v-model="form.uname"
                        :error-messages="errors"
                        label="ID"
                        required
                      ></v-text-field>
                    </validation-provider>
                    <validation-provider
                      rules='required'
                      v-slot="{ errors }"
                      name="password"
                    >
                      <v-text-field 
                        prepend-icon="lock" 
                        v-model="form.upw" 
                        label="Password" 
                        :type="showpw ?'text' :'password'"
                        :append-icon="showpw ? 'mdi-eye' :'mdi-eye-off'"
                        :error-messages="errors"
                        @click:append="showpw = !showpw"
                        @keyup.enter="login"
                      ></v-text-field>
                    </validation-provider>
                  </v-form>
                </validation-observer>
              </v-card-text>
              <v-card-actions>
                <!-- <v-spacer></v-spacer> -->
                <!-- <v-btn
                  text
                  color="error"
                  @click="cancel"
                >
                  취소
                </v-btn> -->
                <v-btn 
                  text
                  color="primary"
                  width="100%"
                  @click="login"
                >
                  <!-- class="ml-10" -->
                  로그인
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import 'material-design-icons-iconfont/dist/material-design-icons.css' 
import myMixin from '../mixins/index'
import {mapActions} from 'vuex'
  export default {
    mixins:[myMixin],
    data(){
      return {
        drawer: null,
        form: {
          uname: null,
          upw: null,
      },
        isLoginError: false,
        showpw:false,
      }
    },
    props: {
      source: String
    },
    methods:{
      ...mapActions(['logIn']),
      async login(){
        const User = new FormData();
        User.append('username', this.form.uname);
        User.append('password', this.form.upw);
        this.$refs.observer.validate()
        .then(val=>{
            if(val){
                this.logIn(User)
                .then(()=>{
                    this.$router.push('/')
                    this.isLoginError=false
                })
                .catch(err=>{
                    this.isLoginError=true
                    console.log(err)
                })
                // const id = this.form.uname;
                // const pw = this.form.upw;
            // this.$http.post('/api/login', {id,pw},{'Content-Type':'application-json'})
            // .then(res=>{
            //   const user = res.data.user;
            //   if (user){
            //     this.$store.commit('setUser',user);
            //     this.$router.push({name:'Home'});
            //   } else {
            //     alert(res.data.message);
            //   }
            // })
            // .catch(err=>{
            //   console.error(err);
            // })
          }
        }
        )
      },
      cancel(){
        this.$router.push('/')
      }
    }
  }
</script>