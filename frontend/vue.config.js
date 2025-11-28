module.exports = {
    chainWebpack: (config) => {
        config.module
            .rule("vue")
            .use("vue-loader")
            .tap((options) => {
                options.compilerOptions = {
                    whitespace: "preserve",
                };
                return options;
            });
    },
};
