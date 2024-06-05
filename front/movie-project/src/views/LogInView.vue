<template>
  <div class="login-container">
    <div class="login-content">
      <h5 class="login-text-box">로그인</h5>
      <form @submit.prevent="logIn" class="login-form">
        <div>
          <input
            class="form-control input-lg"
            type="text"
            v-model.trim="username"
            placeholder="아이디"
          />
        </div>
        <div>
          <input
            class="form-control input-lg"
            type="password"
            v-model.trim="password"
            placeholder="비밀번호"
            id="password"
          />
        </div>
        <button type="submit" class="login-btn btn btn-outline-secondary">
          로그인
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useMovieStore } from "@/stores/counter";

const username = ref(null);
const password = ref(null);
const store = useMovieStore();

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value,
  };
  store.logIn(payload);
};
</script>

<style scoped>
.login-text-box {
  margin-right: 232px;
}
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 220px;
}

.login-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.login-form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.login-form div {
  margin-bottom: 0.65rem; /* 각 입력 필드 간의 간격 */
}

.form-control.input-lg {
  width: 300px; /* 원하는 너비로 설정 */
  padding: 10px;
}

.login-btn {
  width: 300px; /* 버튼 너비 설정 */
  padding: 10px;
  cursor: pointer;
}
</style>
