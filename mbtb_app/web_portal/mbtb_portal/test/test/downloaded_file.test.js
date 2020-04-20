describe("test downloaded file", function () {

  it('file should be downloaded', function () {


    var fs = require('fs');
    var filename='/Users/.../Downloads/MBTB_Data.csv';

    //update contain content
    expect(fs.readFileSync(filename, {encoding: 'utf8'})).toContain("mbtb_code");


    //test filtered csv
    /*expect(fs.readFileSync(filename,{encoding:'utf8'})).not.toContain('not selected parameter');*/

  });
});
