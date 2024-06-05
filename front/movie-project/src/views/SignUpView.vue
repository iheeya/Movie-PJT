<template>
  <p>{{ userList }}</p>
  <div class="signup-container">
    <h5 class="signup-title">
      회원가입으로 영화 추천 서비스를 <br /><span>받을 수 있어요</span>
    </h5>
    <form @submit.prevent="signUp" class="signup-form">
      <input
        class="form-control"
        type="text"
        id="username"
        v-model.trim="username"
        placeholder="유저 이름"
      />
      <input
        class="form-control"
        type="password"
        id="password1"
        v-model.trim="password1"
        placeholder="비밀번호"
      />
      <input
        class="form-control"
        type="password"
        id="password2"
        v-model.trim="password2"
        placeholder="비밀번호 재확인"
      />
      <input type="submit" value="회원가입" class="signup-btn btn btn-outline-secondary"/>
     
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useMovieStore } from "@/stores/counter";

const store = useMovieStore();

const signUp = function () {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
  };
  store.signUp(payload);
};

const username = ref(null);
const password1 = ref(null);
const password2 = ref(null);
</script>

<style scoped>
.signup-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 220px;
}

.signup-title {
  margin-bottom: 20px; /* h1 태그와 폼 사이의 간격 조정 */
}

.signup-form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.form-control {
  width: 320px;
  margin-bottom: 10px; /* 입력 폼 간격 조정 */
}

.signup-btn {
  width: 320px;
  margin-top: 10px; /* 버튼과 마지막 입력 폼 사이의 간격 조정 */
  cursor: pointer;
}

.alert {
  margin-top: 20px;
}
</style>
