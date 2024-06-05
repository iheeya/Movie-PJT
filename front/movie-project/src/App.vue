<template class="full-screen">
  <nav
    class="navbar navbar-expand-lg bg-dark border-bottom border-body navbar-sticky"
    data-bs-theme="dark"
  >
    <div class="container-fluid">
      <RouterLink :to="{ name: 'home' }" class="navbar-brand">
        <i class="fa-solid fa-clapperboard"></i>
      </RouterLink>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNavDropdown"
        aria-controls="navbarNavDropdown"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavDropdown">
        <ul class="navbar-nav flex-grow-1">
          <!-- Apply flex-grow-1 to fill remaining space -->
          <li class="nav-item">
            <RouterLink
              :to="{ name: 'home' }"
              class="nav-link"
              aria-current="page"
              >Home</RouterLink
            >
          </li>


          <!-- Recommend 링크 만들기 -->
          <li class="nav-item">
            <RouterLink
              :to="{ name: 'Recommend' }"
              class="nav-link"
              v-if="store.isLogin"
              aria-current="page"
              >Recommend</RouterLink
            >
          </li>

          <li class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              Category
            </a>
            <ul class="dropdown-menu dropdown-menu-scroll">
              <li v-for="genre in store.genres">
                <RouterLink
                  :to="{ name: 'category', params: { genreId: genre.id } }"
                  class="dropdown-item"
                  >{{ genre.name }}</RouterLink
                >
              </li>
            </ul>
          </li>
        </ul>

        <!-- Move login, sign up, and logout buttons to the right -->
        <div class="navbar-nav ml-auto">
          <li class="nav-item">
            <RouterLink
              :to="{ name: 'SignUpView' }"
              v-if="!store.isLogin"
              class="nav-link"
              aria-current="page"
              >회원가입</RouterLink
            >
          </li>
          <li class="nav-item">
            <form class="d-flex">
              <RouterLink
                :to="{ name: 'LogInView' }"
                v-if="!store.isLogin"
                class="nav-link"
                aria-current="page"
              >
                <button type="submit" class="btn btn-outline-secondary btn-sm">
                  로그인
                </button>
              </RouterLink>
            </form>
          </li>
          <li class="nav-item">
            <RouterLink
              :to="{ name: 'MyProfileView'}"
              v-if="store.isLogin"
              class="nav-link"
              aria-current="page"
              >MY</RouterLink
            >
          </li>
          <li class="nav-item">
            <RouterLink
              @click="store.logOut"
              :to="{ name: 'LogInView' }"
              v-if="store.isLogin"
              class="nav-link"
              aria-current="page"
              >로그아웃</RouterLink
            >
          </li>
        </div>
      </div>
    </div>
  </nav>
  <RouterView />
</template>

<script setup>
import { RouterLink, RouterView } from "vue-router";
import { useMovieStore } from "./stores/counter";
import { onMounted } from "vue";

const store = useMovieStore();

onMounted(() => {
  store.getMovies();
});

onMounted(() => {
  store.getGenres();
});
</script>

<style>
html,
body {
  height: 100%;
  margin: 0;
  background-color: black;
  color: white;
}

.full-screen {
  min-height: 100vh;
}

.container-fluid {
  margin-left: 20px;
}

/* 네비게이션 바 상단 고정 */
.navbar-sticky {
  position: sticky;
  top: 0;
  z-index: 1000; /* 네비게이션 바가 다른 요소 위에 나타나도록 설정 */
}

/* Add this CSS to your styles to enable scrolling within the dropdown */
.dropdown-menu-scroll {
  max-height: 300px; /* Adjust the height as needed */
  overflow-y: auto;
}
</style>
