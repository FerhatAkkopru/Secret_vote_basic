import 'reflect-metadata';
import {
  Mina,
  PrivateKey,
  PublicKey,
  Field,
  AccountUpdate,
} from 'snarkyjs';
import { Voting } from './Voting';

describe('Voting zkApp integration test', () => {
  let feePayer: PrivateKey;
  let zkAppAddress: PublicKey;
  let zkAppPrivateKey: PrivateKey;
  let zkAppInstance: Voting;

  beforeAll(async () => {
    // Local blockchain başlat
    let Local = await Mina.LocalBlockchain({ proofsEnabled: false });
    Mina.setActiveInstance(Local);

    // Test hesabı al
    const account0 = Local.testAccounts[0]!;
    feePayer = account0.privateKey;

    // zkApp hesabı oluştur
    zkAppPrivateKey = PrivateKey.random();
    zkAppAddress = zkAppPrivateKey.toPublicKey();
    zkAppInstance = new Voting(zkAppAddress);

    // Contract deploy et
    let txn = await Mina.transaction(feePayer, async () => {
      AccountUpdate.fundNewAccount(feePayer);
      await zkAppInstance.deploy({ zkappKey: zkAppPrivateKey });
    });
    await txn.prove();
    await txn.sign([feePayer, zkAppPrivateKey]).send();
  });

  it('başlangıçta oylar 0 olmalı', async () => {
    await zkAppInstance.red.fetch();
    await zkAppInstance.blue.fetch();
    await zkAppInstance.green.fetch();
    expect(zkAppInstance.red.get()).toEqual(Field(0));
    expect(zkAppInstance.blue.get()).toEqual(Field(0));
    expect(zkAppInstance.green.get()).toEqual(Field(0));
  });

  it('red için oy verilmeli', async () => {
    let txn = await Mina.transaction(feePayer, async () => {
      await zkAppInstance.vote(
        Field(0),           // kırmızı
        Field(12345),       // person hash (TC+isim+soyisim+yaş)
        Field(1),           // yaş kanıtı
        Field(1),           // person kanıtı
        Field(1)            // oy kanıtı
      );
    });
    await txn.prove();
    await txn.sign([feePayer]).send();

    await zkAppInstance.red.fetch();
    await zkAppInstance.totalVoters.fetch();
    expect(zkAppInstance.red.get()).toEqual(Field(1));
    expect(zkAppInstance.totalVoters.get()).toEqual(Field(1));
  });

  it('blue için oy verilmeli', async () => {
    let txn = await Mina.transaction(feePayer, async () => {
      await zkAppInstance.vote(
        Field(1),           // mavi
        Field(54321),       // person hash (TC+isim+soyisim+yaş)
        Field(1),           // yaş kanıtı
        Field(1),           // person kanıtı
        Field(1)            // oy kanıtı
      );
    });
    await txn.prove();
    await txn.sign([feePayer]).send();

    await zkAppInstance.blue.fetch();
    await zkAppInstance.totalVoters.fetch();
    expect(zkAppInstance.blue.get()).toEqual(Field(1));
    expect(zkAppInstance.totalVoters.get()).toEqual(Field(2));
  });

  it('yaş kontrolü çalışmalı', async () => {
    // 18+ yaş kontrolü
    let txn = await Mina.transaction(feePayer, async () => {
      await zkAppInstance.vote(
        Field(2),           // yeşil
        Field(55555),       // person hash (TC+isim+soyisim+yaş)
        Field(1),           // yaş kanıtı
        Field(1),           // person kanıtı
        Field(1)            // oy kanıtı
      );
    });
    await txn.prove();
    await txn.sign([feePayer]).send();

    await zkAppInstance.green.fetch();
    await zkAppInstance.totalVoters.fetch();
    expect(zkAppInstance.green.get()).toEqual(Field(1));
    expect(zkAppInstance.totalVoters.get()).toEqual(Field(3));
  });

  it('Kişi verileri kontrolü çalışmalı', async () => {
    // Geçerli kişi verileri ile oy verme (güvenli hash ile)
    let txn = await Mina.transaction(feePayer, async () => {
      await zkAppInstance.vote(
        Field(0),           // kırmızı
        Field(44444),       // person hash (TC+isim+soyisim+yaş)
        Field(1),           // yaş kanıtı
        Field(1),           // person kanıtı (geçerli)
        Field(1)            // oy kanıtı (daha önce oy vermemiş)
      );
    });
    await txn.prove();
    await txn.sign([feePayer]).send();

    await zkAppInstance.red.fetch();
    await zkAppInstance.totalVoters.fetch();
    expect(zkAppInstance.red.get()).toEqual(Field(2));
    expect(zkAppInstance.totalVoters.get()).toEqual(Field(4));
  });
});
