import axios from "axios";
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { useRouter } from "vue-router";

export const useMovieStore = defineStore(
  "movie",
  () => {
    const movies = ref([]);
    const genres = ref([]);
    const reviews = ref([]);
    const comments = ref([])

    // const actors = ref([]);
    // const directors = ref([]);
    const API_URL = "http://127.0.0.1:8000";

    const getMovies = function () {
      axios({
        method: "GET",
        url: `${API_URL}/movies/movie_lists/`,
      })
        .then((response) => {
          movies.value = response.data;
          // console.log(movies);
        })
        .catch((error) => {
          console.log(error);
        });
    };

    const getGenres = function () {
      axios({
        method: "GET",
        url: `${API_URL}/movies/genre_lists/`,
      })
        .then((response) => {
          genres.value = response.data;
          console.log(genres);
        })
        .catch((error) => {
          console.log(error);
        });
    };

    const token = ref(null);
    const isLogin = computed(() => {
      if (token.value === null) {
        return false;
      } else {
        return true;
      }
    });

    const router = useRouter();

    const signUp = function (payload) {
      const { username, password1, password2 } = payload;
      axios({
        method: "post",
        url: `${API_URL}/accounts/signup/`,
        data: {
          username,
          password1,
          password2,
        },
      })
        .then((response) => {
          const password = password1;
          this.logIn({ username, password });
        })
        .catch((error) => {
          // console.log(error);
          console.log(error.response.data);
          if (error.response.data['username'] && error.response.data['password1']) {
            alert('이미 존재하는 아이디입니다.');
            alert('비밀번호를 9자이상 입력해주세요');
          } else if (error.response.data['password1']) {
            alert('비밀번호를 9자이상 입력해주세요');
          } else if (error.response.data['non_field_errors']) {
            alert('비밀번호가 일치하지 않습니다')
          } else {
            alert('회원가입에 실패하였습니다.')
          }
          
        });
    };

    const name = ref(null)
    const logIn = function (payload) {
      const { username, password } = payload;
      axios({
        method: "post",
        url: `${API_URL}/accounts/login/`,
        data: {
          username,
          password,
        },
      })
        .then((response) => {
          token.value = response.data.key;
          console.log(response.data.key);
          name.value = response.data.user.username
          router.push({ name: "home" });
        })
        .catch((error) => {
          console.log(error)
          alert('로그인 정보가 일치하지 않습니다')
          
        });
    };

    const logOut = function () {
      token.value = null;
      name.value = null;

      router.push({ name: "LogInView" });
    };


    const getReviews = function () {
      axios({
        method: "GET",
        url: `${API_URL}/reviews/`
      })
        .then((response) => {
          console.log(response);
          reviews.value = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
      }

      const getComments = function () {
        axios({
          method: "GET",
          url: `${API_URL}/comments/create/`
        })
          .then((response) => {
            console.log(response);
            comments.value = response.data;
          })
          .catch((error) => {
            console.log(error);
          });
        }

    const handleSignUp = () => {
      const payload = { username: username.value, password1: password1.value, password2: password2.value };
      movieStore.signUp(payload).catch((error) => {
        errorMessage.value = movieStore.errorMessage;
        showAlert.value = movieStore.showAlert;
      });

    };



    return {
      movies,
      API_URL,
      getMovies,
      genres,
      getGenres,
      signUp,
      token,
      isLogin,
      logIn,
      logOut,
      getReviews,
      reviews,
      name,
      handleSignUp,
      comments,
      getComments,
    };
  },
  { persist: true }
);
