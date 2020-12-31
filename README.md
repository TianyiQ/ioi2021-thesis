## ioi2021-thesis
### 关于这个仓库
- 邱天异的IOI2021集训队论文
- 在仓库结构和格式上参考了EI鸽鸽的仓库[ioi2021-homework](https://github.com/EntropyIncreaser/ioi2021-homework)
### 结构
- `main.tex`: 主文档。无法单独编译。
- `article.tex`: 设置为`ctexart`类型的文档，不包含实质性内容，引用了`main.tex`中的正文。可以正常编译。
- `thesis.tex`: 类似`article.tex`，但是设置为`noithesis`类型（别问我这是啥，我照抄EI鸽鸽的）。无法编译。
- `fig`: 放图片的文件夹。
- `statdata`: 文中用到的统计数据。
- `qty-thesis-statdata.zip`: `statdata`打包得到的文件。
