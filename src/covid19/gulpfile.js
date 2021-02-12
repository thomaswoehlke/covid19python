"use strict";

// Load plugins
const browsersync = require("browser-sync").create();
const del = require("del");
const gulp = require("gulp");
const merge = require("merge-stream");

// BrowserSync
function browserSync(done) {
  browsersync.init({
    server: {
      baseDir: "./"
    },
    port: 3000
  });
  done();
}

// BrowserSync reload
function browserSyncReload(done) {
  browsersync.reload();
  done();
}

// Clean vendor
function clean() {
  return del(["./vendor/"]);
}

// Bring third party dependencies from node_modules into vendor directory
function modules() {
  var bootstrap = gulp.src('./node_modules/bootstrap/dist/**/*')
    .pipe(gulp.dest('./static/vendor/bootstrap'));
  var jquery = gulp.src([
      './node_modules/jquery/dist/*',
      '!./node_modules/jquery/dist/core.js'
    ])
    .pipe(gulp.dest('./static/vendor/jquery'));
  var popper_js = gulp.src([
      './node_modules/popper.js/dist/**/*'
    ])
    .pipe(gulp.dest('./static/vendor/popper.js'));
  var fortawesome_svg_core = gulp.src([
      './node_modules/@fortawesome/fontawesome-svg-core/**/*'
    ])
    .pipe(gulp.dest('./static/vendor/fontawesome-svg-core'));
  var fortawesome_brands_svg_icons = gulp.src([
      './node_modules/@fortawesome/free-brands-svg-icons/**/*'
    ])
    .pipe(gulp.dest('./static/vendor/free-brands-svg-icons'));
  var fortawesome_regular_svg_icons = gulp.src([
      './node_modules/@fortawesome/free-regular-svg-icons/**/*'
    ])
    .pipe(gulp.dest('./static/vendor/free-regular-svg-icons'));
  var fortawesome_solid_svg_icons = gulp.src([
      './node_modules/@fortawesome/free-solid-svg-icons/**/*'
    ])
    .pipe(gulp.dest('./static/vendor/free-solid-svg-icons'));
  return merge(
      bootstrap, jquery, popper_js, fortawesome_svg_core,
      fortawesome_brands_svg_icons, fortawesome_regular_svg_icons, fortawesome_solid_svg_icons
  );
}

// Watch files
function watchFiles() {
  gulp.watch("./**/*.css", browserSyncReload);
  gulp.watch("./**/*.html", browserSyncReload);
}

// Define complex tasks
const vendor = gulp.series(clean, modules);
const build = gulp.series(vendor);
const watch = gulp.series(build, gulp.parallel(watchFiles, browserSync));

// Export tasks
exports.clean = clean;
exports.vendor = vendor;
exports.build = build;
exports.watch = watch;
exports.default = build;
