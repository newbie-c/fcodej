function adjustMenu(data) {
  let menu = {};
  if (data.cu) menu.cu = true;
  if (data.cu.permissions.includes(data.permissions.SEND_PM)) menu.priv = true;
  return menu;
}
