// Preserve the editable group and the style spec's explicit black outline.
export default {
  multipass: true,
  plugins: [{
    name: 'preset-default',
    params: { overrides: {
      collapseGroups: false,
      convertColors: false,
      removeUnknownsAndDefaults: false,
      removeUselessStrokeAndFill: false,
    } },
  }],
};
