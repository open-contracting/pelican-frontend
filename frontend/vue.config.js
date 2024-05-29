module.exports = {
    chainWebpack: (config) => {
        config.module
            .rule("vue")
            .use("vue-loader")
            .tap((options) => {
                options.compiler = require("vue-template-babel-compiler");
                options.compilerOptions.whitespace = "preserve";
                return options;
            });
    },
};
