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
        Field(12345),       // isim hash
        Field(67890),       // soyisim hash
        Field(99999),       // yaş hash
        Field(1)            // yaş kanıtı
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
        Field(54321),       // isim hash
        Field(98765),       // soyisim hash
        Field(88888),       // yaş hash
        Field(1)            // yaş kanıtı
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
        Field(55555),       // isim hash
        Field(66666),       // soyisim hash
        Field(77777),       // yaş hash
        Field(1)            // yaş kanıtı
      );
    });
    await txn.prove();
    await txn.sign([feePayer]).send();

    await zkAppInstance.green.fetch();
    await zkAppInstance.totalVoters.fetch();
    expect(zkAppInstance.green.get()).toEqual(Field(1));
    expect(zkAppInstance.totalVoters.get()).toEqual(Field(3));
  });
});
