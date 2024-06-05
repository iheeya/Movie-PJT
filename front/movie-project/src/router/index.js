import { createRouter, createWebHistory } from "vue-router";
import CategoryView from "@/views/CategoryView.vue";
import MovieDetailView from "@/views/MovieDetailView.vue";
import SignUpView from "@/views/SignUpView.vue";
import LogInView from "@/views/LogInView.vue";
import HomeView from "@/views/HomeView.vue";
import CommunityView from "@/views/CommunityView.vue";
import ProfileView from "@/views/ProfileView.vue";
import ReviewDetailView from "@/views/ReviewDetailView.vue";
import MyProfileView from '@/views/MyProfileView.vue'
import RecommendView from '@/views/RecommendView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/category/:genreId",
      name: "category",
      component: CategoryView,
    },
    {
      path: "/movie/:movieId",
      name: "moive-detail",
      component: MovieDetailView,
    },
    {
      path: "/signup",
      name: "SignUpView",
      component: SignUpView,
    },
    {
      path: "/login",
      name: "LogInView",
      component: LogInView,
    },
    {
      path: "/review/:movieId",
      name: "create-review",
      component: CommunityView,
    },
    {
      path: "/profile/:username",
      name: "ProfileView",
      component: ProfileView,
    },
    {
      path: "/myprofile",
      name: 'MyProfileView',
      component: MyProfileView,
    },
    {
      path: "/detail/:reviewId",
      name: "ReviewDetail",
      component: ReviewDetailView,
    },
    { 
      path: "/recommend",
      name: "Recommend",
      component: RecommendView,
    }
  ],
});

export default router;

// import { useCounterStore } from '@/stores/counter'

// router.beforeEach((to, from) => {
//   const store = useCounterStore()
//   // 인증되지 않은 사용자는 메인 페이지에 접근 할 수 없음
//   if (to.name === 'home' && store.isLogin === false) {
//     window.alert('로그인이 필요해요!!')
//     return { name: 'LogInView' }
//   }

//   // 인증된 사용자는 회원가입과 로그인 페이지에 접근 할 수 없음
//   if ((to.name === 'SignUpView' || to.name === 'LogInView') && (store.isLogin === true)) {
//     window.alert('이미 로그인 했습니다.')
//     return { name: 'home' }
//   }
// })
