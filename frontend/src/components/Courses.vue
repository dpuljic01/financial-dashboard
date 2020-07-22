<template>
  <div class="container">
    <h1>Courses</h1>
    <hr />
    <button type="button" class="btn btn-success btn-sm">Add Course</button>
    <table class="table table-hover">
      <tr>
        <th scope="col">Title</th>
        <th scope="col">Author</th>
        <th scope="col">Paperback</th>
      </tr>
      <tbody>
        <tr v-for="(course, index) in courses" :key="index">
          <td>{{ course.title }}</td>
          <td>{{ course.author }}</td>
          <td>
            <span v-if="course.paperback">Yes</span>
            <span v-else>No</span>
          </td>
          <td>
            <button type="button" class="btn btn-info btn-sm">Update</button>
            <button type="button" class="btn btn-danger btn-sm">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      courses: []
    };
  },
  methods: {
    getCourses() {
      const path = 'http://localhost:5000/api/courses';
      axios
        .get(path)
        .then(res => {
          this.courses = res.data.courses;
        })
        .catch(error => {
          console.error(error);
        });
    }
  },
  created() {
    this.getCourses();
  }
};
</script>
